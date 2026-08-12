import pytest

from smart_todo import main


def test_placeholder_entry_point(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    assert capsys.readouterr().out == "Hello from smart-todo!\n"
