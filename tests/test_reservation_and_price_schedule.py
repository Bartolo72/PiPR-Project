from utils.reservation_and_price_schedule import (
    create_dates,
    create_reservation_json,
    create_price_schedule_json,
    find_price,
    make_reservation
)
from io import StringIO
from classes import Bath
import json
from classes import (
    Individual,
    IndividualType,
    Group,
    Clients,
    DayPart,
    WeekDay,
    PriceSchedule
)
from utils.financial_report import create_income_history


def test_create_dates(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '13 01 2021')
    data = {
        1: [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
        3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    }
    assert create_dates() == (data, 2021)


def test_create_reservation_json(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '13 01 2021')
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    value = json.loads(handle.getvalue())
    year = [int(element) for element in value.keys()]
    assert year[0] == 2021
    january_days = [int(day) for day in value['2021']['1']]
    assert max(january_days) == 31
    assert min(january_days) == 13
    february_days = [int(day) for day in value['2021']['2']]
    assert max(february_days) == 28
    assert min(february_days) == 1


def test_create_price_schedule():
    bath = Bath('Bath', 3, 8, 21)
    normal_morning = IndividualType(15)
    concessionary_morning = IndividualType(12, 'concessionary')
    individual_morning = Individual([normal_morning, concessionary_morning])
    group_morning = Group('group', 70)
    clients_morning = Clients(individual_morning, group_morning)
    morning = DayPart(clients_morning, bath, 'morning', 8, 12)
    normal = IndividualType(20)
    concessionary = IndividualType(17, 'concessionary')
    individual = Individual([normal, concessionary])
    group = Group('group', 90)
    clients = Clients(individual, group)
    normal_dayPart = DayPart(clients, bath)
    day_parts = [normal_dayPart, morning]
    monday = WeekDay(day_parts, 'Monday')
    tuesday = WeekDay(day_parts, 'Tuesday')
    wendsday = WeekDay(day_parts, 'Wendsday')
    thursday = WeekDay(day_parts, 'Thursday')
    friday = WeekDay(day_parts, 'Friday')
    saturday = WeekDay(day_parts, 'Saturday')
    sunday = WeekDay(day_parts, 'Sunday')
    week_days = [monday, tuesday, wendsday, thursday, friday, saturday, sunday]
    price_schedule = PriceSchedule(week_days)
    handle = StringIO()
    create_price_schedule_json(handle, price_schedule)
    value = json.loads(handle.getvalue())
    assert len(value) == 7
    assert len(value['Monday']) == 13
    assert value['Monday']['8']['client type']['individual type']['normal'] == 15
    assert value['Monday']['8']['client type']['group'] == 70
    assert value['Monday']['13']['client type']['individual type']['concessionary'] == 17


def test_find_price():
    bath = Bath('Bath', 3, 8, 21)
    normal_morning = IndividualType(15)
    concessionary_morning = IndividualType(12, 'concessionary')
    individual_morning = Individual([normal_morning, concessionary_morning])
    group_morning = Group('group', 70)
    clients_morning = Clients(individual_morning, group_morning)
    morning = DayPart(clients_morning, bath, 'morning', 8, 12)
    normal = IndividualType(20)
    concessionary = IndividualType(17, 'concessionary')
    individual = Individual([normal, concessionary])
    group = Group('group', 90)
    clients = Clients(individual, group)
    normal_dayPart = DayPart(clients, bath, 'normal', 12)
    day_parts = [morning, normal_dayPart]
    monday = WeekDay(day_parts, 'Monday')
    tuesday = WeekDay(day_parts, 'Tuesday')
    wendsday = WeekDay(day_parts, 'Wendsday')
    thursday = WeekDay(day_parts, 'Thursday')
    friday = WeekDay(day_parts, 'Friday')
    saturday = WeekDay(day_parts, 'Saturday')
    sunday = WeekDay(day_parts, 'Sunday')
    week_days = [monday, tuesday, wendsday, thursday, friday, saturday, sunday]
    price_schedule = PriceSchedule(week_days)
    handle = StringIO()
    create_price_schedule_json(handle, price_schedule)
    value = json.loads(handle.getvalue())
    assert find_price(value, ((13, 1, 2021), 8), 'normal', 1) == 15
    assert find_price(value, ((13, 1, 2021), 11), 'group', 2) == 160


def test_make_reservation(monkeypatch):
    monkeypatch.setattr('reservation_and_price_schedule.today', lambda: '13 01 2021')
    monkeypatch.setattr('date_suggestion.get_date_and_hour', lambda date: ((13, 1, 2021), 20))
    monkeypatch.setattr('reservation_and_price_schedule.confirmation_decision', lambda: True)
    handle = StringIO()
    bath = Bath('Bath', 3, 8, 21)
    create_reservation_json(handle, bath)
    reservations = json.loads(handle.getvalue())
    handle = StringIO()
    normal = IndividualType(15)
    concessionary = IndividualType(12, 'concessionary')
    group = Group('group', 50)
    types = Individual([normal, concessionary])
    clients = Clients(types, group)
    create_income_history(clients, handle)
    income = json.loads(handle.getvalue())
    normal_morning = IndividualType(15)
    concessionary_morning = IndividualType(12, 'concessionary')
    individual_morning = Individual([normal_morning, concessionary_morning])
    group_morning = Group('group', 70)
    clients_morning = Clients(individual_morning, group_morning)
    morning = DayPart(clients_morning, bath, 'morning', 8, 12)
    normal = IndividualType(20)
    concessionary = IndividualType(17, 'concessionary')
    individual = Individual([normal, concessionary])
    group = Group('group', 90)
    clients = Clients(individual, group)
    normal_dayPart = DayPart(clients, bath, 'normal', 12)
    day_parts = [morning, normal_dayPart]
    monday = WeekDay(day_parts, 'Monday')
    tuesday = WeekDay(day_parts, 'Tuesday')
    wendsday = WeekDay(day_parts, 'Wendsday')
    thursday = WeekDay(day_parts, 'Thursday')
    friday = WeekDay(day_parts, 'Friday')
    saturday = WeekDay(day_parts, 'Saturday')
    sunday = WeekDay(day_parts, 'Sunday')
    week_days = [monday, tuesday, wendsday, thursday, friday, saturday, sunday]
    price_schedule_obj = PriceSchedule(week_days)
    handle = StringIO()
    create_price_schedule_json(handle, price_schedule_obj)
    price_schedule = json.loads(handle.getvalue())
    make_reservation('group', reservations, 3, bath, income, price_schedule)
    assert reservations['2021']['1']['14']['1']['8'] == 'group'
    assert reservations['2021']['1']['14']['1']['9'] == 'group'
    assert reservations['2021']['1']['14']['1']['10'] == 'group'
    assert income['group'] == 210
    assert income['individual type']['normal'] == 0
    assert income['individual type']['concessionary'] == 0
    make_reservation('normal', reservations, 2, bath, income, price_schedule)
    assert reservations['2021']['1']['14']['2']['8'] == 4
    assert reservations['2021']['1']['14']['2']['9'] == 4
    assert income['individual type']['normal'] == 30
    assert income['individual type']['concessionary'] == 0
