from calendar import Calendar
from datetime import date
import json
from utils.date_suggestion import (
    suggest_for_groups,
    suggest_for_clients
)
from utils.financial_report import set_income_from


def today():
    today = date.today().strftime("%d %m %Y")
    return today


def create_dates():
    """
    1. Load present date
    2. Create list of current month days
    3. Create dict which values are lists of month days - [<current_day>, ..., <last_month_day>]
     also this dict should have up to 2 following months
    """
    today_str = today()
    day, month, year = [int(element) for element in today_str.split()]
    calendar = Calendar()
    dates = {}
    n = 0
    while n < 3:
        if n == 0:
            new_day = day
        curr_month_days = [int(day) for day in calendar.itermonthdays(year, month)]
        dates[month] = [element for element in range(day, max(curr_month_days) + 1)]
        day = 1
        month += 1
        n += 1
    dates[month] = [element for element in range(1, new_day + 1)]
    return dates, year


def add_curr_date_to_json(file_handle):
    """
    1. Take current date
    2. Iterate through existing json file
    3. Add date to json file, when at the end of the month create new dict of consecutive month and then add the date
    """
    pass


def create_reservation_json(file_handle, baths):
    """
    baths - Bath object
    dates - dict = {<month>: [<day>, ...] }
    1. Load <dates>, <year> from create_dates()
    2. Create dict available_hours = {<hour>: <availability>}
    3. Create dict available_line = {<line>: available_hours}
    4. Create dict data = {<year>: {<month>: <available_line}}
    5. Save to json file
    """
    dates, year = create_dates()
    opening = baths.opening_hour()
    closing = baths.closing_hour()
    lines = baths.line_amount()
    available_hours = {i: 5 for i in range(opening, closing)}
    available_line = {i: available_hours for i in range(1, lines + 1)}
    data = {year: {}}
    months = {}
    for month in dates:
        days = [day for day in dates[month]]
        days_dict = {day: available_line for day in days}
        months[month] = days_dict
    data[year] = months
    json.dump(data, file_handle, indent=4)


def create_week_days():
    """
    used only if there is no week days list
    """
    pass


def set_hour_with_day_parts(week_day):
    """
    week_day - WeekDay object
    1. Create hour dict = {<opening>: <price>,
                            ...,
                            <closing>: <price>
                            }
    2. Check whether hour is in specific day_part
    3. Create dict for each hour:
    hours = {<hour>: {
            clients_types: {
                individual: {
                    <type>: <price_for_hour>
                    }
                groups: <price_for_hour>
                }
            }
        }
    }
    4. Return hours dict
    """
    opening = week_day.day_parts[0].bath.opening_hour()
    closing = week_day.day_parts[0].bath.closing_hour()
    hours = {hour: {} for hour in range(opening, closing)}
    for hour in hours:
        for day_part in week_day.day_parts:
            if hour in range(day_part.part_opening_hour, day_part.part_closing_hour):
                data = {'client type': {
                    'individual type': day_part.clients.individual.types_with_prices(),
                    'group': day_part.clients.groups.price
                }}
                hours[hour] = data
    return hours


def create_price_schedule_json(file_handle, price_schedule):
    """
    for each week day create dict with set_hour_with_prices
    """
    data = {}
    for day in price_schedule.week_days:
        data[day.name] = set_hour_with_day_parts(day)
    json.dump(data, file_handle, indent=4)


def display_price(price):
    return print(f"Reservation will cost {price}zl")


def find_week_day(date):
    """
    date = (day, month, year)
    return the number of week day 0 - Monday
    """
    calendar = Calendar()
    day, month, year = date
    month_week_days = [day for day in calendar.itermonthdays2(year, month)]
    for day_desc in month_week_days:
        if day_desc[0] == day:
            return day_desc[1]


def find_price(price_schedule, date, client, reservation_length):
    """
    client - 'groups' or type of indivual client (also str)
    1. Go to price schedule and find date ((<day>, <month>, <year>), hour)
    2. Calculate the price for reservation
    3. Return price for reservation
    """
    week_days = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wendsday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    price = []
    number = find_week_day(date[0])
    hour = date[1]
    if client == 'group':
        for i in range(0, reservation_length):
            price_for_hour = price_schedule[week_days[number]][str(hour)]['client type']['group']
            price.append(price_for_hour)
            hour += 1
    else:
        for i in range(0, reservation_length):
            price_for_hour = price_schedule[week_days[number]][str(hour)]['client type']['individual type'][client]
            price.append(price_for_hour)
            hour += 1
    return sum(price)


def confirmation_decision():
    decision = input('Do you want to confrim your reservation? Y/N: ')
    if decision == 'Y':
        return True
    else:
        return False


def confirmed_reservation(date, reservations, clients, line, reservation_length):
    """
    ((day, month, year), hour) = date
    1. Go to specific date in reservations
    2. Decrement it's availability or change it the 'group'
    3. return that reservation is confirmed
    """
    day, month, year = date[0]
    if confirmation_decision():
        if reservation_length == 1:
            if clients == 'group':
                reservations[str(year)][str(month)][str(day)][str(line)][str(date[1])] = 'group'
            else:
                reservations[str(year)][str(month)][str(day)][str(line)][str(date[1])] -= 1
        else:
            hour_number = int(date[1])
            for hour in range(0, reservation_length):
                if clients == 'group':
                    reservations[str(year)][str(month)][str(day)][str(line)][str(hour_number)] = 'group'
                    hour_number += 1
                else:
                    reservations[str(year)][str(month)][str(day)][str(line)][str(hour_number)] -= 1
                    hour_number += 1
        print('Reservation has been confirmed')
        return


def make_reservation(client_type, reservations, reservation_length, bath, income, price_schedule):
    if client_type == 'group':
        result = suggest_for_groups(reservations, reservation_length, bath)
        """
        result = desc, ((day, month, year), hour, reservation_length), line
        """
        print(result[0])
        price = find_price(price_schedule, (result[1][0], result[1][1]), client_type, reservation_length)
        display_price(price)
        confirmed_reservation((result[1][0], result[1][1]), reservations, 'group', result[2], reservation_length)
        set_income_from('group', price, income)
    else:
        result = suggest_for_clients(reservations, reservation_length, bath)
        print(result[0])
        price = find_price(price_schedule, (result[1][0], result[1][1]), client_type, reservation_length)
        display_price(price)
        confirmed_reservation((result[1][0], result[1][1]), reservations, client_type, result[2], reservation_length)
        set_income_from(client_type, price, income)
