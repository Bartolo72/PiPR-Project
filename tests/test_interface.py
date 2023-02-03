from interface import (
    bath_check,
    bath_creator,
    create_clients_for_day_part_standard,
    create_specific_day_part,
    path_check,
    client_type
)
from classes import (
    Bath,
    IndividualType,
    Individual,
    Group,
    Clients
)


def test_bath_check():
    bath = Bath('Pływalnia', 3, 8, 21)
    assert bath_check(None) is False
    assert bath_check(bath) is True


def test_bath_creator(monkeypatch):
    monkeypatch.setattr('interface.bath_opening', lambda: 8)
    monkeypatch.setattr('interface.bath_closing', lambda x: 20)
    monkeypatch.setattr('interface.line_amount_bath', lambda: 5)
    monkeypatch.setattr('interface.bath_name', lambda: 'BATH')
    bath = bath_creator()
    assert bath.name() == 'BATH'
    assert bath.opening_hour() == 8
    assert bath.closing_hour() == 20
    assert bath.line_amount() == 5


def test_create_clients_standard_day_part(monkeypatch):
    normal = IndividualType(15)
    ind = Individual([normal])
    group = Group('group', 50)
    monkeypatch.setattr('interface.create_individual_clients_standard', lambda: ind)
    monkeypatch.setattr('interface.create_group', lambda: group)
    clients = create_clients_for_day_part_standard()
    assert clients.individual == ind
    assert clients.groups == group


def test_specific_day_part_creator(monkeypatch):
    normal = IndividualType(15)
    normal_v2 = IndividualType(13)
    ind = Individual([normal])
    ind_2 = IndividualType([normal_v2])
    group = Group('group', 50)
    clients = Clients(ind, group)
    new_clients = Clients(ind_2, group)
    bath = Bath('Pływalnia', 3, 8, 21)
    monkeypatch.setattr('interface.create_clients_specific_day_part', lambda x, y, z: new_clients)
    monkeypatch.setattr('interface.specific_day_part_questions', lambda bath: ('morning', 8, 12))
    day_part = create_specific_day_part(bath, clients)
    assert day_part.name == 'morning'
    assert day_part.part_opening_hour == 8
    assert day_part.part_closing_hour == 12


def test_path_check(monkeypatch):
    open('price_schedule.json', 'w')
    monkeypatch.setattr('interface.path_name', lambda: 'price_schedule.json')
    assert path_check() == 'price_schedule.json'


def test_path_check_false(monkeypatch):
    monkeypatch.setattr('interface.path_name', lambda: 'not_existing.json')
    assert path_check() is False


def test_client_type(monkeypatch):
    monkeypatch.setattr('interface.choose_client_number', lambda clients: 1)
    clients = {
                'individual type': {
                    'normal': 15,
                    'not normal': 12
                    },
                'groups': 45
                }
    client = client_type(clients)
    assert client == 'normal'

