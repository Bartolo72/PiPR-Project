from utils.financial_report import (
    create_income_history,
    set_income_from,
    calculate_income,
    create_report,
    display_report
)
from io import StringIO
from classes import (
    Clients,
    Group,
    Individual,
    IndividualType
)
import json


def test_create_income_history():
    handle = StringIO()
    normal = IndividualType(15)
    concessionary = IndividualType(12, 'concessionary')
    group = Group('group', 50)
    types = Individual([normal, concessionary])
    clients = Clients(types, group)
    create_income_history(clients, handle)
    value = json.loads(handle.getvalue())
    assert len(value['individual type']) == 2
    assert value['individual type']['normal'] == 0
    assert value['individual type']['concessionary'] == 0
    assert value['group'] == 0


def test_set_income_from():
    handle = StringIO()
    normal = IndividualType(15)
    concessionary = IndividualType(12, 'concessionary')
    group = Group('group', 50)
    types = Individual([normal, concessionary])
    clients = Clients(types, group)
    create_income_history(clients, handle)
    value = json.loads(handle.getvalue())
    set_income_from('group', 100, value)
    set_income_from('group', 150, value)
    set_income_from('normal', 45, value)
    assert value['group'] == 250
    assert value['individual type']['normal'] == 45


def test_calculate_income():
    handle = StringIO()
    normal = IndividualType(15)
    concessionary = IndividualType(12, 'concessionary')
    group = Group('group', 50)
    types = Individual([normal, concessionary])
    clients = Clients(types, group)
    create_income_history(clients, handle)
    value = json.loads(handle.getvalue())
    set_income_from('group', 100, value)
    set_income_from('group', 150, value)
    set_income_from('normal', 45, value)
    income = calculate_income(value)
    assert income == 295


def _create_report():
    handle = StringIO()
    normal = IndividualType(15)
    concessionary = IndividualType(12, 'concessionary')
    group = Group('group', 50)
    types = Individual([normal, concessionary])
    clients = Clients(types, group)
    create_income_history(clients, handle)
    value = json.loads(handle.getvalue())
    set_income_from('group', 100, value)
    set_income_from('group', 150, value)
    set_income_from('normal', 45, value)
    report = create_report('15/01/2021', value)
    display_report(report)


_create_report()