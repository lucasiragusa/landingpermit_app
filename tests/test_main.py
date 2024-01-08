import pytest
import pendulum
from pathlib import Path
from src.utils.pendulum_helper import parse_date, pendulum_to_string, get_week_signature, get_weekday, get_year, get_week_number, get_date_range, reformat_date_signature

import sys
print(sys.path)

@pytest.mark.parametrize("date_str, expected_date", [
    ("01May23", pendulum.datetime(2023, 5, 1)),
    ("12Dec22", pendulum.datetime(2022, 12, 12)),
])
def test_parse_date(date_str, expected_date):
    assert parse_date(date_str) == expected_date
    
@pytest.mark.parametrize("date_str, expected_signature", [
    ("01May23", "2023_18"),  
    ("12Dec22", "2022_50"),  
])
def test_get_week_signature(date_str, expected_signature):
    assert get_week_signature(date_str) == expected_signature

@pytest.mark.parametrize("date_obj, expected_weekday", [
    (pendulum.datetime(2023, 5, 1), 1), 
    (pendulum.datetime(2022, 12, 12), 1),  
])
def test_get_weekday(date_obj, expected_weekday):
    assert get_weekday(date_obj) == expected_weekday

@pytest.mark.parametrize("date_str, expected_year", [
    ("01May23", 2023),
    ("12Dec22", 2022),
])
def test_get_year(date_str, expected_year):
    assert get_year(date_str) == expected_year

@pytest.mark.parametrize("date_str, expected_week_number", [
    ("01May23", 18),  
    ("12Dec22", 50),  
])
def test_get_week_number(date_str, expected_week_number):
    assert get_week_number(date_str) == expected_week_number

@pytest.mark.parametrize("start_date_str, end_date_str, expected_range", [
    ("01May23", "07May23", 7),  
    ("01Dec22", "31Dec22", 31),  
])
def test_get_date_range(start_date_str, end_date_str, expected_range):
    assert get_date_range(start_date_str, end_date_str) == expected_range

@pytest.mark.parametrize("date_obj, expected_str", [
    (pendulum.datetime(2023, 5, 1), "01May23"),
    (pendulum.datetime(2022, 12, 12), "12Dec22"),
])
def test_pendulum_to_string(date_obj, expected_str):
    assert pendulum_to_string(date_obj) == expected_str

@pytest.mark.parametrize("date_str, expected_format", [
    ("01JAN23", "01Jan23"),
    ("15FEB22", "15Feb22"),
])
def test_reformat_date_signature(date_str, expected_format):
    if expected_format:
        assert reformat_date_signature(date_str) == expected_format
    else:
        with pytest.raises(ValueError):
            reformat_date_signature(date_str)
