from twttr import shorten


def test_shorten_basic():
    assert shorten("Hello World") == "Hll Wrld"

def test_shorten_capitalized():
    assert shorten("AEIOUaeiou") == ""

def test_shorten_numbers():
    assert shorten("CS50") == "CS50"

def test_shorten_punctuation():
    assert shorten ("CS50,a") == "CS50,"
