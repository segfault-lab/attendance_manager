from enum import StrEnum


class Weekday(StrEnum):
    MON = "monday"
    TUE = "tuesday"
    WED = "wednesday"
    THU = "thursday"
    FRI = "friday"
    SAT = "saturday"
    SUN = "sunday"


class Grade(StrEnum):
    GOLD = "GOLD"
    SILVER = "SILVER"
    NORMAL = "NORMAL"

