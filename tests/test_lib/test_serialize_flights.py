from src.lib.serialize_flights import parse_date

import pytest

@pytest.mark.parametrize("datestr, expected",
[
    ("sunday", True),
    ("sunday", False),
])
def test_parse_date(datestr, expected):
    result = parse_date(date_str=datestr)

    assert result == expected