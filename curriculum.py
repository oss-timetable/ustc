import asyncio
import os
import aiohttp
from tqdm import tqdm

from models.course import Course
from models.semester import Semester
from utils.catalog import login as catalog_login
from utils.catalog import get_semesters, get_courses, get_exams
from utils.jw import login as jw_login
from utils.jw import update_lectures
from utils.tools import save_json, save_course_markdown

base_path = os.path.dirname(os.path.abspath(__file__))
API_PATH = os.path.join(base_path, "build", "api")
API_SEMESTER_PATH = os.path.join(API_PATH, "semester")
API_COURSE_PATH = os.path.join(API_PATH, "course")
MARKDOWN_COURSE_PATH = os.path.join(base_path, "build", "markdown", "course")

for path in [API_SEMESTER_PATH, API_COURSE_PATH, MARKDOWN_COURSE_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)


async def fetch_course_info(session, semester, courses, sem, progress_bar):
    async with sem:
        courses = await update_lectures(session, courses)
        for course in courses:
            save_json(course, os.path.join(API_COURSE_PATH, f"{course.id}"))
            save_course_markdown(
                semester, course, os.path.join(MARKDOWN_COURSE_PATH, f"{course.id}.md")
            )

        progress_bar.update(len(courses))


async def fetch_semester(session, semester):
    courses = await get_courses(session, semester.id)
    save_json(courses, os.path.join(API_SEMESTER_PATH, semester.id))

    if int(semester.id) >= 321:
        exams = await get_exams(session, semester.id)
        for course in courses:
            if course.id in exams.keys():
                course.exams = exams[course.id]

    sem = asyncio.Semaphore(10)
    progress_bar = tqdm(
        total=len(courses),
        position=0,
        leave=True,
        desc=f"Processing {semester.name}",
    )
    course_chunks = [courses[i : i + 50] for i in range(0, len(courses), 50)]
    tasks = [
        fetch_course_info(session, semester, course_chunk, sem, progress_bar)
        for course_chunk in course_chunks
    ]
    with progress_bar:
        await asyncio.gather(*tasks)


async def make_curriculum():
    async with aiohttp.ClientSession() as session:
        await catalog_login(session)
        await jw_login(session)

        semesters = await get_semesters(session=session)
        semesters = [semester for semester in semesters if int(semester.id) >= 141]
        save_json(semesters, os.path.join(API_PATH, "semesters"))

        for semester in tqdm(
            semesters, position=1, leave=True, desc="Processing semesters"
        ):
            await fetch_semester(session, semester)


def main():
    asyncio.run(make_curriculum())


if __name__ == "__main__":
    main()
