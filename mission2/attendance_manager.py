from typing import Dict
from mission2.constants import Weekday, Grade
from mission2.user import User, UserFactory
from mission2.rule import DAY_POINTS, DefaultStrategy, BONUS_RULES


class AttendanceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AttendanceManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.users: Dict[str, User] = {}
            self.factory = UserFactory()
            self.grade_strategy = DefaultStrategy()
            self.initialized = True

    def register_user(self, username: str) -> User:
        if username not in self.users:
            self.users[username] = self.factory.create(username)
        return self.users[username]

    def record_attendance(self, username: str, weekday: str) -> None:
        try:
            day_enum = Weekday(weekday.lower())
        except ValueError:
            return
        user = self.register_user(username)
        user.attendance[day_enum] += 1
        user.points += DAY_POINTS[day_enum]

    def calculate_grade(self) -> None:
        for user in self.users.values():
            self.grade_strategy.apply(user)
            for rule in BONUS_RULES:
                user.points += rule(user)

    def removed_users(self):
        return [
            user
            for user in self.users.values()
            if user.grade == Grade.NORMAL
            and user.attendance[Weekday.WED] == 0
            and (user.attendance[Weekday.SAT] + user.attendance[Weekday.SUN]) == 0
        ]

    def display_results(self) -> None:
        for user in self.users.values():
            print(f"NAME : {user.name}, POINT : {user.points}, GRADE : {user.grade}")

        print("\nRemoved player\n==============")
        for user in self.removed_users():
            print(user.name)
