from datetime import date, datetime
from utils.reservation_and_price_schedule import (
    create_price_schedule_json,
    create_reservation_json,
    make_reservation
)
from classes import (
    Bath,
    Individual,
    IndividualType,
    Clients,
    Group,
    DayPart,
    WeekDay,
    PriceSchedule,
    InvalidHour
)
from utils.financial_report import (
    create_income_history,
    create_report,
    display_report
)
import json


def bath_check(bath):
    """
    check whether bath object exist
    """
    if bath is not None:
        return True
    else:
        return False


def bath_opening():
    right = True
    while right:
        try:
            hour = int(input('What time does your bath open?\nEnter the hour: '))
            if hour not in range(0, 23):
                raise InvalidHour
            right = False
            return hour
        except Exception:
            print('Please type correct hour')


def bath_closing(opening):
    right = True
    while right:
        try:
            hour = int(input(f'What time does your bath close?\nOpening: {opening}\nEnter the hour: '))
            if hour not in range(opening, 24):
                raise TypeError(f'Enter the hour between {opening}-23')
            right = False
            return hour
        except Exception:
            print('Please type correct hour')


def line_amount_bath():
    right = True
    while right:
        try:
            line_amount = int(input('How many lines does your bath have?\nEnter the number: '))
            right = False
            return line_amount
        except Exception:
            print('Invalid line number')


def bath_name():
    name = input('Enter the name of your bath: ')
    return name


def bath_creator():
    """
    create the object Bath
    """
    name = bath_name()
    opening_hour = bath_opening()
    closing_hour = bath_closing(opening_hour)
    line_amount = line_amount_bath()
    bath = Bath(name, line_amount, opening_hour, closing_hour)
    return bath


def price_schedule_check():
    """
    Check whether price schedule exist
    """
    path = price_schedule_existance()
    if path is not False:
        return path
    else:
        return False


def reservations_check():
    """
    Check whether reservation history exist
    """
    path = reservations_existance()
    if path is not False:
        return path
    else:
        return False


def specific_day_part_decision():
    if input("Do you want to create specific day part? Y/N: ") == 'Y':
        return True
    else:
        return False


def price_schedule_creator(bath):
    """
    1. Create all types of clients for the interface usage
    2. Than create day_parts for each day in week day
    3. Return
    """
    normal = create_standard_day_part(bath)
    day_parts = [normal]
    if specific_day_part_decision():
        right = True
        while right:
            day_part = create_specific_day_part(bath, normal.clients)
            day_parts.append(day_part)
            if input('Add another one? Y/N: ') != 'Y':
                right = False
    week_days = create_week_days(day_parts, bath, normal.clients)
    price_schedule = PriceSchedule(week_days)
    return price_schedule


def create_individual_clients_standard():
    types = []
    right = True
    while right:
        name = input('Enter the name of the individual client type: ')
        price_h = int(input('Price for one hour: '))
        types.append(IndividualType(price_h, name))
        if input('Add another one? Y/N: ') != 'Y':
            right = False
    ind_clients = Individual(types)
    return ind_clients


def create_group():
    group_name = input('Enter the name of the group client: ')
    group_price = int(input('Price for one hour: '))
    group = Group(group_name, group_price)
    return group


def create_clients_for_day_part_standard():
    individual = create_individual_clients_standard()
    group = create_group()
    clients = Clients(individual, group)
    return clients


def display_week_days(week_days_numbers):
    """
    week_days_numbers = [(number, week_day),...]
    """
    for week_day in week_days_numbers:
        desc = f"{week_day[0]}. {week_day[1]}"
        print(desc)


def create_week_days(day_parts, bath, clients):
    """
    day_parts - list of DayPart object
    """
    week_days = ['Monday', 'Tuesday', 'Wendsday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_days_numbers = list(enumerate(week_days, 1))
    week_days_obj = []
    if not input('Do you want to use created day parts to all week days? Y/N: ') == 'Y':
        right = True
        while right:
            display_week_days(week_days_numbers)
            number = int(input('Enter the number of the day which you want to specify: '))
            print('Creating default day part')
            normal_day_part = create_standard_day_part(bath)
            right_v2 = True
            day_parts = [normal_day_part]
            if input(f'Do you want to add specific day part at {week_days[number - 1]}? Y/N: ') == 'Y':
                while right_v2:
                    day_part = create_specific_day_part(bath, clients)
                    day_parts.append(day_part)
                    if not input('Add another day part? Y/N: ') == 'Y':
                        right_v2 = False
            for day in week_days_numbers:
                if day[0] == number:
                    week_day = WeekDay(day_parts, day[0])
                    week_days_obj.append(week_day)
                    week_days_numbers.remove(day)
            if not input("Do you want to specify another day? Y/N: ") == 'Y':
                right = False
    for week_day in week_days:
        week_day = WeekDay(day_parts, week_day)
        week_days_obj.append(week_day)
    return week_days_obj


def create_clients_specific_day_part(clients, opening, closing):
    individual_types = []
    for _type in clients.individual.types:
        print(f"Individual type client: {_type.name}")
        price = int(input('Enter the price for one hour: '))
        ind_type = IndividualType(price, _type.name)
        individual_types.append(ind_type)
    print('Group:')
    price = int(input("Enter the price for one hour: "))
    group = Group(clients.groups.name, price)
    new_individual = Individual(individual_types)
    new_clients = Clients(new_individual, group)
    return new_clients


def create_standard_day_part(bath):
    """
    We need this if we want to create another day parts
    """
    clients = create_clients_for_day_part_standard()
    normal = DayPart(clients, bath)
    return normal


def hour_range(_open, close):
    right = True
    while right:
        print(f"Bath opening hours: {_open}-{close}")
        hour = int(input("Enter the hour: "))
        if hour in range(_open, close):
            right = False
            return hour
        if hour not in range(_open, close):
            print(f"Enter the hour between {_open}-{close}")


def specific_day_part_questions(bath):
    name = input('Creating specific day part.\nEnter the name of this day part: ')
    print("Day part starting hour: ")
    opening = hour_range(bath.opening_hour(), bath.closing_hour())
    print('Day part closing hour: ')
    closing = hour_range(bath.opening_hour(), bath.closing_hour())
    return (name, opening, closing)


def create_specific_day_part(bath, clients):
    """
    after creating basic/standard day part we can use this function
    to create another one for example if we want te create morning day part
    """
    name, opening, closing = specific_day_part_questions(bath)
    new_clients = create_clients_specific_day_part(clients, opening, closing)
    day_part = DayPart(new_clients, bath, name, opening, closing)
    return day_part


def checklist(bath=None):
    """
    if price_schedule is not false than the price_schedule = path
    """
    price_schedule = price_schedule_check()
    reservations = reservations_check()
    if not bath_check(bath):
        bath = bath_creator()
    if not price_schedule:
        with open('price_schedule.json', 'w') as handle:
            price_schedule = price_schedule_creator(bath)
            create_price_schedule_json(handle, price_schedule)
            price_schedule = 'price_schedule.json'
    if not reservations:
        with open('reservations.json', 'w') as handle:
            create_reservation_json(handle, bath)
            reservations = 'reservations.json'
    return bath, json.load(open(price_schedule)), json.load(open(reservations))


def path_name():
    path = input('Enter the file name: ')
    return path


def path_check():
    """
    if file already exists ask of the path to that file
    """
    right = True
    while right:
        try:
            path = path_name()
            with open(path):
                right = False
                return path
        except FileNotFoundError:
            print('File not found')
            return False


def reservations_existance():
    existance = input('Do you have reservations file? Y/N: ')
    if existance == 'Y':
        path = path_check()
        return path
    else:
        return False


def price_schedule_existance():
    existance = input('Do you have price schedule file? Y/N: ')
    if existance == 'Y':
        path = path_check()
        return path
    else:
        return False


def create_clients_from_price_schedule(price_schedule, bath):
    clients_ind_dict = price_schedule['Monday'][str(bath.opening_hour())]['client type']['individual type']
    clients_ind = [IndividualType(0, name) for name in clients_ind_dict.keys()]
    individual = Individual(clients_ind)
    group = Group('group', 0)
    clients = Clients(individual, group)
    return clients


def display_options(options):
    for option in options:
        print(f"{option}.{options[option]}")


def display_client_types(clients):
    """
    clients = [(number, name), ...]
    """
    print('Client types:')
    for client in clients:
        print(f"{client[0]}. {client[1]}")


def client_type(clients):
    """
    clients = {
                individual type: {
                    <type>: <price_for_hour>
                    }
                groups: <price_for_hour>
                }
    display client types
    return the given client type
    """
    new_clients = [str(name) for name in clients['individual type'].keys()]
    new_clients.append('group')
    clients_numbers = list(enumerate(new_clients, 1))
    number = choose_client_number(clients_numbers)
    for client in clients_numbers:
        if client[0] == number:
            return client[1]


def choose_client_number(clients):
    display_client_types(clients)
    number = int(input('Choose your client type number: '))
    return number


def back_to_menu():
    if input('Go back to the menu? Y/N: ') == 'Y':
        return True
    else:
        return False


def launching_func(bath=None):
    launching = {
        'date': '19 01 2021',
        'launched': False
    }
    """
    Only an idea to automaticly check whther program was used in a following day, now it is manually
    By default program will ask for needed files and then perform func interface()
    '''
    launching = json.load(open('launching.json'))
    launching[today]['launched'] = 0
    '''
    after using interface
    '''
    launching[today]['launched'] += 1
    '''
    """
    today = date.today().strftime("%d %m %Y")
    data = []
    if launching['date'] == today and launching[today] is False:
        bath, price_schedule, reservations = checklist(bath)
        clients = create_clients_from_price_schedule(price_schedule, bath)
        with open('income.json', 'w') as handle:
            create_income_history(clients, handle)
        income = json.load(open('income.json'))
        data = [bath, price_schedule, reservations, income]
        interface(bath, price_schedule, reservations, income)
    if launching['date'] != today:
        bath, price_schedule, reservations = checklist(bath)
        clients = create_clients_from_price_schedule(price_schedule, bath)
        with open('income.json', 'w') as handle:
            create_income_history(clients, handle)
        income = json.load(open('income.json'))
        data = [bath, price_schedule, reservations, income]
        interface(bath, price_schedule, reservations, income)
        launching['date'] = today
        launching['launched'] = True
    if launching['date'] == today and launching['launched'] is True:
        interface(data[0], data[1], data[2], data[3])


def interface(bath, price_schedule, reservations, income):
    """
    1.Display your options
    2.Go to option and execute
    3.Ask whether you want to continue
    """
    hour = datetime.now().hour
    today = date.today().strftime("%d %m %Y")
    options = {
        1: 'Make a reservation',
        2: 'Display price schedule',
        3: 'Modify price schedule',
        4: 'Financial report',
        5: 'Exit'
    }
    right = True
    while right:
        display_options(options)
        number = int(input("Enter the action number: "))
        if number == 1:
            cl_type = client_type(price_schedule['Monday'][str(bath.opening_hour())]['client type'])
            reservation_length = int(input('Enter reservation length: '))
            make_reservation(cl_type, reservations, reservation_length, bath, income, price_schedule)
            if not back_to_menu():
                right = False
        if number == 2:
            print(price_schedule)
            if not back_to_menu():
                right = False
        if number == 3:
            print('Action not available yet')
            if not back_to_menu():
                right = False
        if number == 4:
            if hour == (bath.closing_hour() - 1):
                report = create_report(today, income)
                display_report(report)
                if not back_to_menu():
                    right = False
            else:
                print('Only available when the last hour of opening is started')
                if not back_to_menu():
                    right = False
        if number == 5:
            if input('Are you sure? Y/N: ') == 'Y':
                right = False


if __name__ == '__main__':
    bath = Bath('Pływalnia', 3, 8, 21)
    launching_func(bath)
