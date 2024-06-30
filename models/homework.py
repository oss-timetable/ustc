from typing import Optional


class Homework:
    name: str
    index: int
    deadline: Optional[int]  # unix timestamp
    content: str
    contentHTML: str

    def __init__(
        self,
        name: str,
        index: int,
        deadline: Optional[int],
        content: str,
        contentHTML: str,
    ):
        self.name = name
        self.index = index
        self.deadline = deadline
        self.content = content
        self.contentHTML = contentHTML
