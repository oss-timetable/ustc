import jsonpickle
from datetime import datetime, timedelta
from pytz import timezone
from jinja2 import Template, Environment

from models.course import Course
from models.semester import Semester

tz = timezone("Asia/Shanghai")


def raw_date_to_unix_timestamp(date_str: str, format="%Y-%m-%d") -> int:
    dt = datetime.strptime(date_str, format)
    tz_aware_datetime = tz.localize(dt)
    return int(tz_aware_datetime.timestamp())


def parse_header(raw: str) -> dict:
    return {i.split(": ")[0]: i.split(": ")[1] for i in raw.split("\n")[1:-1]}


def save_json(obj: any, path: str):
    with open(path, "w") as f:
        f.write(jsonpickle.encode(obj, indent=4))

def load_json(path: str, type: any):
    with open(path, "r") as f:
        return jsonpickle.decode(f.read(), classes=type)


def unix_timestamp_to_date_str(timestamp: int, format: str = "%Y-%m-%d %H:%M"):
    return datetime.fromtimestamp(timestamp, tz).strftime(format)


def save_course_markdown(semester: Semester, course: Course, path: str):
    env = Environment()
    env.filters["unix_timestamp_to_date_str"] = unix_timestamp_to_date_str
    with open("./utils/templates/course.md", "r") as f:
        template = env.from_string(f.read())

    with open(path, "w") as f:
        f.write(template.render(semester=semester, course=course))
