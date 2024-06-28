from typing import Optional


class Homework:
    name: str
    index: int
    deadline: Optional[int]  # unix timestamp
    content: str

    def __init__(self, name: str, index: int, deadline: Optional[int], content: str):
        self.name = name
        self.index = index
        self.deadline = deadline
        self.content = content
