import pytest
from mission1.attendance import main as mission1
from mission2.main import main as mission2


@pytest.mark.parametrize("main_func", [mission1, mission2])
def test_main(main_func, capsys):
    input_file = "attendance_weekday_500.txt"
    expected_output = "tests/answer.txt"
    main_func(input_file)
    captured = capsys.readouterr()
    with open(expected_output, "r", encoding="utf-16") as f:
        answer = f.read()
    assert captured.out == answer


@pytest.mark.parametrize("main_func", [mission1, mission2])
def test_invalid_file(main_func, capsys):
    main_func("dummy.txt")
    captured = capsys.readouterr()
    assert "파일을 찾을 수 없습니다." in captured.out
