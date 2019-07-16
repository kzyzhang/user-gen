from user_gen import user_gen
from user_gen import age_calculate
import sys
import re
import pytest
import datetime


def test_age_calculate():
    date = datetime.datetime(2019, 7, 15)
    assert age_calculate(datetime.datetime(1957, 7, 15), date) == 62
    assert age_calculate(datetime.datetime(1957, 7, 14), date) == 62
    assert age_calculate(datetime.datetime(1957, 7, 26), date) == 61
    assert age_calculate(datetime.datetime(1957, 3, 12), date) == 62
    assert age_calculate(datetime.datetime(1957, 12, 15), date) == 61
    assert age_calculate(datetime.datetime(1958, 7, 16), date) == 60
    assert age_calculate(datetime.datetime(1958, 7, 14), date) == 61


def test_user_gen():
    users = user_gen(10)
    # print(users)
    for user in users:

        assert "@" and "." in user["email"]
        assert type(user["age"]) == int
        assert len(user["dob"]) == 10


@pytest.mark.parametrize(
    "test_input",
    [
        ("78y8"),
        (" "),
        ("adsf"),
        ("ads4asf3y8a"),
        (" sd , df,2"),
        ("£$%^&*&^"),
        ("a215"),
    ],
)
def test_validate_input_wrong(test_input):
    p = re.compile("^[0-9]+$")
    assert p.match(test_input) == None


@pytest.mark.parametrize(
    "test_input", [("788"), ("2"), ("222333323234234324324"), ("1")]
)
def test_validate_input_right(test_input):
    regex = re.compile("^[0-9]+$")
    assert regex.match(test_input) != None
