from typing import Dict, Callable
from mission2.constants import Weekday, Grade
from mission2.user import User

# Bonus points configuration
WEEKEND_ATTENDANCE_THRESHOLD = 9
WEEKEND_BONUS_POINTS = 10
WEDNESDAY_ATTENDANCE_THRESHOLD = 9
WEDNESDAY_BONUS_POINTS = 10

DAY_POINTS: Dict[Weekday, int] = {
    Weekday.MON: 1,
    Weekday.TUE: 1,
    Weekday.WED: 3,
    Weekday.THU: 1,
    Weekday.FRI: 1,
    Weekday.SAT: 2,
    Weekday.SUN: 2,
}

GRADE_THRESHOLDS = {
    Grade.GOLD: 50,
    Grade.SILVER: 30,
    Grade.NORMAL: 0,
}


class GradeStrategy:
    def apply(self, user: User) -> None:
        raise NotImplementedError


class DefaultStrategy(GradeStrategy):
    def apply(self, user: User) -> None:
        points = user.points
        if points >= GRADE_THRESHOLDS[Grade.GOLD]:
            user.grade = Grade.GOLD
        elif points >= GRADE_THRESHOLDS[Grade.SILVER]:
            user.grade = Grade.SILVER
        else:
            user.grade = Grade.NORMAL

        user.points = points


def bonus_rule(func: Callable[[User], int]):
    def wrapper(user: User) -> int:
        return func(user)

    return wrapper


@bonus_rule
def midweek_bonus(user: User) -> int:
    return WEDNESDAY_BONUS_POINTS if user.attendance[Weekday.WED] > WEDNESDAY_ATTENDANCE_THRESHOLD else 0


@bonus_rule
def weekend_bonus(user: User) -> int:
    return WEEKEND_BONUS_POINTS if user.attendance[Weekday.SAT] + user.attendance[
        Weekday.SUN] > WEEKEND_ATTENDANCE_THRESHOLD else 0


BONUS_RULES = [midweek_bonus, weekend_bonus]
