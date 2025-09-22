from mission2.constants import Weekday, Grade
from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    attendance: dict[Weekday, int] = field(default_factory=lambda: {day: 0 for day in Weekday})
    points: int = 0
    grade: Grade = Grade.NORMAL


class UserFactory:
    def __init__(self):
        self.counter = 0

    def create(self, username: str) -> User:
        self.counter += 1
        return User(id=self.counter, name=username)
