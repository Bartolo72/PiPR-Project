import classes
import pytest


def test_bath():
    bath = classes.Bath('Pływalnia', 5, 8, 21)
    assert bath.name() == 'Pływalnia'
    assert bath.line_amount() == 5
    assert bath.opening_hour() == 8
    assert bath.closing_hour() == 21


def test_invalid_hour():
    with pytest.raises(classes.InvalidHour):
        classes.Bath('Bath', 5, 52, 25)


def test_day_part_no_hour_given():
    bath = classes.Bath('Bath', 5, 8, 21)
    morning = classes.DayPart('clients', bath, 'morning')
    assert morning.name == 'morning'
    assert morning.part_opening_hour == 8
    assert morning.part_closing_hour == 21


def test_day_part_one_hour_given():
    bath = classes.Bath('Bath', 5, 8, 21)
    evening = classes.DayPart("clients", bath, 'evening', 18)
    assert evening.part_opening_hour == 18
    assert evening.part_closing_hour == 21


def test_day_part_no_name():
    bath = classes.Bath('Bath', 5, 8, 21)
    evening = classes.DayPart("clients", bath)
    assert evening.name == 'normal'


def test_date_invalidDay():
    with pytest.raises(classes.InvalidDay):
        classes.Date(32)


def test_date_invalidMonth():
    with pytest.raises(classes.InvalidMonth):
        classes.Date(12, 14)


def test_date_invalidYear():
    with pytest.raises(classes.InvalidYear):
        classes.Date(12, 12, 2020)
