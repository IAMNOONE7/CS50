from bank import value


def test_bank_hello():
    assert value("Hello asd") == 0
    assert value("hello asd") == 0

def test_bank_hi():
    assert value("Hi asd") == 20
    assert value("hi asd") == 20

def test_bank_other():
    assert value("Asd Hello") == 100
    assert value("asd hello") == 100
