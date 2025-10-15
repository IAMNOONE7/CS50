from um import count


def test_count_legit():
    assert count("um UM uM Um") == 4
    assert count("UM?") == 1

def test_count_subs():
    assert count("um yummy") == 1
    assert count("yummy trum") == 0
    
