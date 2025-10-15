from fuel import convert, gauge
import pytest


def test_gauge():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(75) == "75%"


def test_convert():
    assert convert("1/2") == 50
    assert convert("3/4") == 75

def test_convert_exceptions():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")

    with pytest.raises(ValueError):
        convert("2/1")

    with pytest.raises(ValueError):
        convert("-1/4")
