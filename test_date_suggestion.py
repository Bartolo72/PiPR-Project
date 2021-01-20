from date_suggestion import (
    hour_format,
    date_description,
    get_date_and_hour,
    date_split,
    availability_check_clients,
    availability_check_groups,
    group_amount_check,
    suggest_for_clients,
    suggest_for_groups
)
from reservation_and_price_schedule import create_reservation_json
import datetime
from classes import Bath, Date, InvalidHour
import pytest
from io import StringIO
import json


def test_hour_format():
    assert hour_format(12, 24) == 13
    assert hour_format(12, 00) == 12


def test_date_description():
    today = datetime.date.today().strftime("%d %m %Y")
    day, month, year = [int(element) for element in today.split()]
    assert date_description((day, month, year), 17, 2, 3)[0] == f"Line: 3 is available for 2 hours Date:{day}/{month:02}/{year} Start:17:00"
    assert date_description((day, month, year), 17, 1, 3)[0] == f"Line: 3 is available for 1 hour Date:{day}/{month:02}/{year} Start:17:00"


def test_get_date_and_hour_choosen_hour(monkeypatch):
    monkeypatch.setattr('date_suggestion.booking_day', lambda: True)
    monkeypatch.setattr('date_suggestion.choosing_hour', lambda: True)
    monkeypatch.setattr('date_suggestion.type_hour', lambda: 12)
    today = datetime.date.today().strftime("%d %m %Y")
    day, month, year = [int(element) for element in today.split()]
    bath = Bath('Pływalnia', 5, 8, 21)
    result = get_date_and_hour(bath)
    assert result == ((day, month, year), 12)


def test_get_date_and_hour_invalid_hour(monkeypatch):
    monkeypatch.setattr('date_suggestion.booking_day', lambda: True)
    monkeypatch.setattr('date_suggestion.choosing_hour', lambda: True)
    monkeypatch.setattr('date_suggestion.type_hour', lambda: 24)
    bath = Bath('Pływalnia', 5, 8, 21)
    with pytest.raises(InvalidHour):
        get_date_and_hour(bath)


def test_get_date_and_hour_not_choosen_hour(monkeypatch):
    monkeypatch.setattr('date_suggestion.booking_day', lambda: True)
    monkeypatch.setattr('date_suggestion.choosing_hour', lambda: False)
    today = datetime.date.today().strftime("%d %m %Y")
    day, month, year = [int(element) for element in today.split()]
    bath = Bath('Pływalnia', 5, 8, 21)
    curr_hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    hour = hour_format(curr_hour, minute)
    assert get_date_and_hour(bath) == ((day, month, year), hour)


def test_get_date_and_hour_not_booking_day(monkeypatch):
    monkeypatch.setattr('date_suggestion.booking_day', lambda: False)
    monkeypatch.setattr('date_suggestion.choosing_hour', lambda: False)
    bath = Bath('Pływalnia', 5, 8, 21)
    today = datetime.date.today().strftime("%d %m %Y")
    day, month, year = [int(element) for element in today.split()]
    date = Date(day, month, year)
    monkeypatch.setattr('date_suggestion.get_date', lambda: date)
    assert get_date_and_hour(bath) == ((date.day, date.month, date.year), 8)


def test_date_split_1():
    date_str = '14'
    date = date_split(date_str)
    assert date.day == 14


def test_date_split_2():
    date_str = '14/03'
    date = date_split(date_str)
    assert date.month == 3


def test_date_split_3():
    date_str = '14/03/2022'
    date = date_split(date_str)
    assert date.year == 2022


def test_availability_check_clients():
    data = {
        '1': {
            '8': 'group',
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 1,
            '13': 0
        },
        '2': {
            '8': 0,
            '9': 3,
            '10': 'group',
            '11': 5,
            '12': 3,
            '13': 5
        },
        '3': {
            '8': 0,
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 5,
            '13': 0
        }
    }
    bath = Bath('BATH', 3, 8, 13)
    assert availability_check_clients(data, 1, bath, 8) == (False, [])
    assert availability_check_clients(data, 3, bath, 8) == (False, [])


def test_group_amount_check():
    data = {
        '1': {
            '8': 'group',
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 1,
            '13': 0
        },
        '2': {
            '8': 0,
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 1,
            '13': 0
        },
        '3': {
            '8': 5,
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 1,
            '13': 0
        }
    }
    bath = Bath('BATH', 3, 8, 13)
    assert group_amount_check(data, 8, bath) is True
    assert group_amount_check(data, 9, bath) is True
    assert group_amount_check(data, 10, bath) is False


def test_availability_chek_groups():
    data = {
        '1': {
            '8': 'group',
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 1,
            '13': 0
        },
        '2': {
            '8': 0,
            '9': 3,
            '10': 'group',
            '11': 5,
            '12': 3,
            '13': 5
        },
        '3': {
            '8': 5,
            '9': 3,
            '10': 'group',
            '11': 2,
            '12': 5,
            '13': 0
        }
    }
    bath = Bath('BATH', 3, 8, 14)
    assert availability_check_groups(data, 2, bath, 8) == (False, [])


def test_date_suggestion_clients_another_line(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '13 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((13, 1, 2021), 19))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['13']['1']['19'] = 0
    value['2021']['1']['13']['1']['20'] = 0
    date_desc = suggest_for_clients(value, 1, bath)
    assert date_desc[0] == 'Line: 2 is available for 1 hour Date:13/01/2021 Start:19:00'


def test_date_suggestion_clients_another_day(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '13 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((13, 1, 2021), 20))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['13']['1']['20'] = 0
    value['2021']['1']['13']['2']['20'] = 0
    value['2021']['1']['13']['3']['20'] = 0
    date_desc = suggest_for_clients(value, 1, bath)
    assert date_desc[0] == 'Line: 1 is available for 1 hour Date:14/01/2021 Start:8:00'


def test_date_suggestion_clients_another_month(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '31 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((31, 1, 2021), 20))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['31']['1']['20'] = 0
    value['2021']['1']['31']['2']['20'] = 0
    value['2021']['1']['31']['3']['20'] = 0
    date_desc = suggest_for_clients(value, 1, bath)
    assert date_desc[0] == 'Line: 1 is available for 1 hour Date:1/02/2021 Start:8:00'


def test_date_suggestion_clients_length2(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '31 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((31, 1, 2021), 19))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['31']['1']['20'] = 0
    value['2021']['1']['31']['3']['20'] = 0
    value['2021']['1']['31']['2']['20'] = 0
    date_desc = suggest_for_clients(value, 2, bath)
    assert date_desc[0] == 'Line: 1 is available for 2 hours Date:1/02/2021 Start:8:00'


def test_date_suggestion_groups(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '30 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((30, 1, 2021), 20))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['30']['1']['20'] = 0
    value['2021']['1']['30']['3']['20'] = 'group'
    date_desc = suggest_for_groups(value, 1, bath)
    assert date_desc[0] == 'Line: 2 is available for 1 hour Date:30/01/2021 Start:20:00'
    date_desc_2 = suggest_for_groups(value, 2, bath)
    assert date_desc_2[0] == 'Line: 1 is available for 2 hours Date:31/01/2021 Start:8:00'


def test_date_suggestion_groups_next_day(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '30 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((30, 1, 2021), 20))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['30']['1']['20'] = 0
    value['2021']['1']['30']['3']['20'] = 'group'
    value['2021']['1']['30']['2']['20'] = 'group'
    date_desc = suggest_for_groups(value, 3, bath)
    assert date_desc[0] == 'Line: 1 is available for 3 hours Date:31/01/2021 Start:8:00'


def test_date_suggestion_groups_next_month(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '31 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((31, 1, 2021), 20))
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    value['2021']['1']['31']['1']['20'] = 0
    value['2021']['1']['31']['3']['20'] = 'group'
    value['2021']['1']['31']['2']['20'] = 'group'
    date_desc = suggest_for_groups(value, 3, bath)
    assert date_desc[0] == 'Line: 1 is available for 3 hours Date:1/02/2021 Start:8:00'