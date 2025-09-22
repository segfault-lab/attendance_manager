import pytest
from mission2.attendance_manager import AttendanceManager
from mission2.constants import Weekday, Grade
from mission2.user import User, UserFactory
from mission2.rule import DAY_POINTS, WEDNESDAY_BONUS_POINTS, WEEKEND_BONUS_POINTS, BONUS_RULES, weekend_bonus, midweek_bonus


@pytest.fixture(autouse=True)
def reset_all():
    AttendanceManager._instance = None
    yield


def test_user_factory_create_unique_ids():
    factory = UserFactory()
    user1 = factory.create("user1")
    user2 = factory.create("user2")
    assert user1.id != user2.id
    assert isinstance(user1, User)


def test_register_user():
    manager = AttendanceManager()
    manager.record_attendance("user", "monday")
    manager.record_attendance("user", "wednesday")
    manager.record_attendance("user", "saturday")

    user = manager.users["user"]
    assert user.attendance[Weekday.MON] == 1
    assert user.attendance[Weekday.WED] == 1
    assert user.attendance[Weekday.SAT] == 1
    assert user.points == DAY_POINTS[Weekday.MON] + DAY_POINTS[Weekday.WED] + DAY_POINTS[Weekday.SAT]


def test_invalid_day():
    manager = AttendanceManager()
    user_name = "user"
    manager.record_attendance(user_name, "noday")
    assert user_name not in manager.users


@pytest.mark.parametrize("user_name, day, count, expected_grade",
                         [("user1", "monday", 29, Grade.NORMAL),
                          ("user2", "tuesday", 30, Grade.SILVER),
                          ("user3", "thursday", 49, Grade.SILVER),
                          ("user4", "friday", 50, Grade.GOLD)], )
def test_default_grade_strategy(user_name, day, count, expected_grade):
    manager = AttendanceManager()
    for _ in range(count):
        manager.record_attendance(user_name, day)
    manager.calculate_grade()
    assert manager.users[user_name].grade == expected_grade


def test_bonus_strategy():
    user_name = "user"
    manager = AttendanceManager()
    for _ in range(10):
        manager.record_attendance(user_name, "wednesday")
        manager.record_attendance(user_name, "saturday")

    manager.calculate_grade()
    user = manager.users[user_name]
    assert midweek_bonus(user) == 10
    assert weekend_bonus(user) == 10
    assert all(callable(rule) for rule in BONUS_RULES)
    assert user.grade == Grade.GOLD
    assert user.points == 50 + WEDNESDAY_BONUS_POINTS + WEEKEND_BONUS_POINTS


def test_removed_users_detection():
    manager = AttendanceManager()
    user_name = "user"
    manager.record_attendance(user_name, "monday") # weekday only
    manager.calculate_grade()
    removed = manager.removed_users()
    assert manager.users[user_name] in removed


def test_display_results_and_removed_users(capsys):
    manager = AttendanceManager()
    user_name = "user"
    manager.record_attendance(user_name, "monday")
    manager.calculate_grade()
    manager.display_results()

    captured = capsys.readouterr()
    assert f"NAME : {user_name}" in captured.out
    assert "Removed player" in captured.out


def test_singleton_property():
    manager1 = AttendanceManager()
    manager2 = AttendanceManager()
    assert manager1 is manager2