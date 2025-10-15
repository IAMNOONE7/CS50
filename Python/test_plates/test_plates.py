from plates import is_valid

def test_plates_legit():
    assert is_valid("CS50") == True
    assert is_valid("50CS") == False
    assert is_valid("C50") == False
    
def test_plates_zero_first():
    assert is_valid("CS05") == False

def test_plates_letter_last():
    assert is_valid("CS50P") == False

def test_plates_dot():
    assert is_valid("PI3.14") == False

def test_plates_short():
    assert is_valid("H") == False

def test_plates_long():
    assert is_valid("OUTATIME") == False
