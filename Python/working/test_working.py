from working import convert
import pytest

def test_convert_legit():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("8:42 AM to 2:35 PM") == "08:42 to 14:35"
    assert convert("5:37 PM to 12:22 AM") == "17:37 to 00:22"


def test_convert_value_error():
    with pytest.raises(ValueError):
        convert("9am to 5pm")
    with pytest.raises(ValueError):
        convert("14 am to 5pm")
    with pytest.raises(ValueError):
        convert("20 AM to 13 PM")
    with pytest.raises(ValueError):
        convert("9 am - 5pm")
    with pytest.raises(ValueError):
        convert("0 am to 5pm")
