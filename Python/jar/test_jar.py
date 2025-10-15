import pytest
from jar import Jar


def test_init():
    jar = Jar()

    assert jar.capacity == 12
    assert jar.size ==0

    jar1 = Jar(5)
    assert jar1.capacity == 5

    with pytest.raises(ValueError):
        jar2 = Jar(-1)

def test_str():
    jar=Jar()
    assert str(jar) == ""

    jar.deposit(1)
    assert str(jar) == "🍪"

    jar.deposit(3)
    assert str(jar) == "🍪"*4

def test_deposit():
    jar = Jar(5)
    jar.deposit(3)
    assert jar.size == 3

    with pytest.raises(ValueError):
        jar.deposit(10)

def test_withdraw():
    jar = Jar(5)
    jar.deposit(4)
    jar.withdraw(1)
    assert jar.size == 3

    with pytest.raises(ValueError):
        jar.withdraw(10)



