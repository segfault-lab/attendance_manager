import sys
from mission2.attendance_manager import AttendanceManager


def main(filename: str) -> None:
    system = AttendanceManager()
    try:
        with open(filename) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    system.record_attendance(parts[0], parts[1])

        system.calculate_grade()
        system.display_results()
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    main("../attendance_weekday_500.txt")
