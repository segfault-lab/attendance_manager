from enum import StrEnum
from typing import Dict
from collections import namedtuple


class Weekday(StrEnum):
    MON = "monday"
    TUE = "tuesday"
    WED = "wednesday"
    THU = "thursday"
    FRI = "friday"
    SAT = "saturday"
    SUN = "sunday"


DAY_POINTS: Dict[Weekday, int] = {
    Weekday.MON: 1,
    Weekday.TUE: 1,
    Weekday.WED: 3,
    Weekday.THU: 1,
    Weekday.FRI: 1,
    Weekday.SAT: 2,
    Weekday.SUN: 2,
}


class Grade(StrEnum):
    GOLD = "GOLD"
    SILVER = "SILVER"
    NORMAL = "NORMAL"


GRADE_THRESHOLDS = {
    Grade.GOLD: 50,
    Grade.SILVER: 30,
    Grade.NORMAL: 0,
}


User = namedtuple("User", ["id", "attendance", "points", "grade"])

users: Dict[str, User] = {}
user_counter: int = 0


def create_user(user_id: int) -> User:
    return User(
        id=user_id,
        attendance={day: 0 for day in Weekday},
        points=[0],
        grade=[Grade.NORMAL],
    )


def register_user(username: str) -> User:
    global user_counter
    if username not in users:
        user_counter += 1
        users[username] = create_user(user_counter)
    return users[username]


def record_attendance(username: str, weekday: str) -> None:
    day_enum = Weekday(weekday.lower())
    user = register_user(username)
    user.attendance[day_enum] += 1
    user.points[0] += DAY_POINTS[day_enum]


def calculate_grades() -> None:
    for username, user in users.items():
        points = user.points[0]
        att = user.attendance

        if att[Weekday.WED] > 9:
            points += 10
        if att[Weekday.SAT] + att[Weekday.SUN] > 9:
            points += 10

        if points >= GRADE_THRESHOLDS[Grade.GOLD]:
            user.grade[0] = Grade.GOLD
        elif points >= GRADE_THRESHOLDS[Grade.SILVER]:
            user.grade[0] = Grade.SILVER
        else:
            user.grade[0] = Grade.NORMAL

        user.points[0] = points


def is_removed_user(user: User) -> bool:
    return (
        user.grade[0] == Grade.NORMAL
        and user.attendance[Weekday.WED] == 0
        and (user.attendance[Weekday.SAT] + user.attendance[Weekday.SUN]) == 0
    )


def display_results() -> None:
    # Display all users and their grades
    for username, user in users.items():
        print(
            f"NAME : {username}, POINT : {user.points[0]}, GRADE : {user.grade[0]}"
        )

    # Display removed users
    print("\nRemoved player\n==============")
    for username, user in users.items():
        if is_removed_user(user):
            print(f"{username}")


def main(filename: str) -> None:
    try:
        with open(filename) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    record_attendance(parts[0], parts[1])

        calculate_grades()
        display_results()
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    main("../attendance_weekday_500.txt")
