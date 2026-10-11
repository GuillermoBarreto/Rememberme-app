"""Unit tests for rememberme's --interval-minutes parsing (no GUI needed)."""

import pytest

import rememberme


def test_default_interval_is_sixty_minutes():
    assert rememberme._parse_interval_minutes(["rememberme.py"]) == 60


def test_custom_interval_space_form():
    assert (
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes", "10"])
        == 10
    )


def test_custom_interval_equals_form():
    assert (
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes=15"])
        == 15
    )


def test_missing_value_exits_2():
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes"])
    assert exc.value.code == 2


def test_empty_equals_value_exits_2():
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes="])
    assert exc.value.code == 2


@pytest.mark.parametrize("bad", ["abc", "0", "-5"])
def test_invalid_values_exit_2(bad):
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes", bad])
    assert exc.value.code == 2


def test_equals_form_non_numeric_value_exits_2():
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--interval-minutes=abc"])
    assert exc.value.code == 2


def test_unknown_flag_exits_2(capsys):
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--inteval-minutes", "10"])
    assert exc.value.code == 2
    assert "unknown option" in capsys.readouterr().err


def test_help_flag_exits_0(capsys):
    with pytest.raises(SystemExit) as exc:
        rememberme._parse_interval_minutes(["rememberme.py", "--help"])
    assert exc.value.code == 0
    assert "usage:" in capsys.readouterr().out
