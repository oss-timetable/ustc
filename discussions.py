import requests
import re

from utils.environs import GITHUB_TOKEN
from utils.tools import raw_date_to_unix_timestamp
from models.homework import Homework


def fetch_github_discussions(owner, repo):
    url = "https://api.github.com/graphql"

    def fetch_page(cursor=None):
        cursor_str = f', after: "{cursor}"' if cursor else ""
        query = """
        {
            repository(owner: "%s", name: "%s") {
                discussions(first: 100%s) {
                    nodes {
                        title
                        url
                        comments(first: 100) {
                            nodes {
                                body
                                author {
                                    login
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """ % (owner, repo, cursor_str)

        headers = {
            "Authorization": f"bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {"query": query}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch discussions: {response.status_code}, {response.text}"
            )

    discussions = []
    cursor = None

    while True:
        result = fetch_page(cursor)
        page_discussions = result["data"]["repository"]["discussions"]["nodes"]
        for discussion in page_discussions:
            all_comments = []
            comment_cursor = None
            while True:
                comments_page = discussion['comments']
                all_comments.extend(comments_page['nodes'])
                if not comments_page['pageInfo']['hasNextPage']:
                    break
                comment_cursor = comments_page['pageInfo']['endCursor']
                discussion['comments'] = fetch_page(comment_cursor)["data"]["repository"]["discussions"]["nodes"][0][
                    'comments']
            discussion['comments']['nodes'] = all_comments
        discussions.extend(page_discussions)
        if not result["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]:
            break
        cursor = result["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]

    return discussions


def parse_homework_from_comment(body: str) -> Homework:
    # for title the following format are supported:
    # #*HW \d+:
    # #*HW\d+:
    # #*Homework \d+:
    # #*Homework\d+:

    # an optional second line could be used to indicate the deadline:
    # ddl: YYYY-MM-DD HH:MM
    # which is considered to be in UTF-8 by default

    # the rest are considered content for the homework

    lines = body.splitlines()

    if len(lines) < 2:
        raise ValueError("Invalid lines")

    title_regex = re.compile(r"#* *(HW|Homework|hw|homework) *(\d+):?")
    if not title_regex.match(lines[0]):
        raise ValueError("Title format not supported")

    # use match group 2 as id:
    id = title_regex.match(lines[0]).group(2)

    # try match ddl line, if not, set ddl to none
    ddl_regex = re.compile(">? *(ddl|DDL):? *(\d{4}-\d{2}-\d{2} \d{2}:\d{2})")
    ddl = None

    content = "\n".join(lines[1:])
    if ddl_regex.match(lines[1]):
        if len(lines) < 3:
            raise ValueError("Invalid lines")

        ddl_text = ddl_regex.match(lines[1]).group(2)
        ddl = raw_date_to_unix_timestamp(ddl_text, format="%Y-%m-%d %H:%M")
        content = "\n".join(lines[2:])

    return Homework(name=f"Homework {id}", index=int(id), deadline=ddl, content=content)


def main():
    owner = "oss-timetable"
    repo = "ustc"

    result = {}

    discussions = fetch_github_discussions(owner, repo)
    for discussion in discussions:
        if discussion is None:
            continue
        course_id_search = re.search(r"\d+", discussion["title"])
        if course_id_search is None:
            continue
        course_id = course_id_search.group()
        homeworks = []

        for comment in discussion["comments"]["nodes"]:
            if "author" not in comment or comment["author"] is None:
                continue

            body = comment['body']
            try:
                homework = parse_homework_from_comment(body)
                homeworks.append(homework)
            except Exception as e:
                continue

        if len(homeworks) > 0:
            result[course_id] = homeworks

    return result


if __name__ == "__main__":
    print(main())
