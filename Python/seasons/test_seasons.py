import pytest
from datetime import date, timedelta
from seasons import calculate_minutes

def test_calculate_minutes_yesterday():
    yesterday = date.today() - timedelta(days=1)
    assert "One thousand, four hundred forty minutes" in calculate_minutes(yesterday)

def test_calculate_minutes_2_days():
    yesterday = date.today() - timedelta(days=2)
    assert "Two thousand, eight hundred eighty minutes" in calculate_minutes(yesterday)

def test_calculate_2_years():
    two_years = date.today() - timedelta(days = 730)
    assert "One million, fifty-one thousand, two hundred minutes" in calculate_minutes(two_years)

def test_calculate_1_years():
    one_year = date.today() - timedelta(days = 365)
    assert "Five hundred twenty-five thousand, six hundred minutes" in calculate_minutes(one_year)
