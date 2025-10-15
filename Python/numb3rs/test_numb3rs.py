from numb3rs import validate

def test_validate_legit():
    assert validate("0.0.0.0")
    assert validate("1.2.3.4")
    assert validate("255.255.255.255")


def test_validate_range():
    assert not validate("256.1.1.1")
    assert not validate("-1.1.1.1")
    assert not validate("255.300.1.1")
    assert not validate("1000.1.1.1")
    assert not validate("10.0.001.203")

def test_validate_random():
    assert not validate("asd")
    assert not validate("256,1,1,1")
    assert not validate("256.1.1.1")
    assert not validate(".1.1.1.1")
