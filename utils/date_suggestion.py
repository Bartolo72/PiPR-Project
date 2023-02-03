from calendar import Calendar
from classes import InvalidHour, Date
import datetime


def hour_format(hour, minutes):
    """
    Round hours to full hour
    """
    if minutes == 0:
        return hour
    else:
        return hour + 1


def date_description(date, hour, reservation_length, line):
    time = 'hour' if reservation_length == 1 else 'hours'
    desc = f"Line: {line} is available for {reservation_length} {time} Date:{date[0]}/{date[1]:02}/{date[2]} Start:{hour}:00"
    return desc, (date, hour, reservation_length), line


def booking_day():
    decision = input("Do you want to book it today? Y/N: ")
    if decision == 'Y':
        return True
    else:
        return False


def type_hour():
    hour = input("Type hour: ")
    return int(hour)


def date_split(date):
    date_int = [int(element) for element in date.split('/')]
    if len(date_int) == 1:
        date = Date(date_int[0])
    if len(date_int) == 2:
        date = Date(date_int[0], date_int[1])
    if len(date_int) == 3:
        date = Date(date_int[0], date_int[1], date_int[2])
    return date


def get_date():
    print("() means it is optional")
    given_date = input('Date format: <day>(/<month>/)(/<year>)\nType date: ')
    date = date_split(given_date)
    return date


def choosing_hour():
    decision = input("Do you want to choose specific hour? Y/N: ")
    if decision == "Y":
        return True
    else:
        return False


def get_date_and_hour(bath):
    """
    1. Ask whether you want to book today or any other day
    2. Ask for specific hour if today otherwise it should load current hour rounding it (ex. 12:23 - 13)
    3. If not today ask about specific date, where typing month and year is optional - we assume
    that when month and year are None we take current month and year
    4. Return (day, month, year), hour
    """
    today = datetime.date.today().strftime("%d %m %Y")
    day, month, year = [int(element) for element in today.split()]
    reservation_day = booking_day()
    if reservation_day:
        decision = choosing_hour()
        if decision:
            hour = type_hour()
            if hour not in range(bath.opening_hour(), bath.closing_hour()):
                raise InvalidHour()
        else:
            curr_hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute
            hour = hour_format(curr_hour, minute)
    if not reservation_day:
        date = get_date()
        decision = choosing_hour()
        if decision:
            hour = type_hour()
            if hour not in range(bath.opening_hour(), bath.closing_hour()):
                raise InvalidHour()
        else:
            hour = bath.opening_hour()
        return (date.day, date.month, date.year), hour
    return (day, month, year), hour


def availability_check_clients(data, length, bath, start_hour):
    """
    data = {<line>: {<hour>: availability}}
    Check whtether there are <length> following, available hours
    """
    for line in data:
        availability_length = 0
        reservation_hours = []
        for hour in range(start_hour, (start_hour + length)):
            if hour == bath.closing_hour():
                break
            if data[str(line)][str(hour)] != 0 and data[str(line)][str(hour)] != 'group':
                availability_length += 1
                reservation_hours.append(int(hour))
                if length == availability_length:
                    return True, reservation_hours, line
            else:
                availability_length = 0
                if len(reservation_hours) != 0:
                    reservation_hours.clear()
    return False, reservation_hours


def group_amount_check(data, hour, bath):
    """
    data = {<line>: {<hour>: availability}}
    """
    group_amount = 0
    for line in data:
        if data[line][str(hour)] == 'group':
            group_amount += 1
    if float(group_amount/bath.line_amount()) >= 0.35:
        return False
    else:
        return True


def availability_check_groups(data, length, bath, start_hour):
    """
    data = {<line> {<hour>: <availability>}}
    """
    for line in data:
        availability_length = 0
        reservation_hours = []
        for hour in range(start_hour, (start_hour + length)):
            if hour == bath.closing_hour():
                break
            if group_amount_check(data, hour, bath):
                if data[line][str(hour)] == 5:
                    availability_length += 1
                    reservation_hours.append(int(hour))
                    if length == availability_length:
                        return True, reservation_hours, line
                else:
                    availability_length = 0
                    if len(reservation_hours) != 0:
                        reservation_hours.clear()
    return False, reservation_hours


def current_month_days(month, year):
    calendar = Calendar()
    return [int(day) for day in calendar.itermonthdays(year, int(month))]


def suggest_for_clients(data, reservation_length, bath):
    """
    data - reservation history
    1. Load current date, hour and length of reservation
    2. Go to reservaion history at given date and hour
    3. Divide due to reservation_length (int in hours)
    4. If no reservation at given day go to next day
    5. Check whether the line is available for reservation_length hours -
    if True display
    """
    date, hour = get_date_and_hour(bath)
    day_number = date[0]
    if reservation_length == 1:
        for month in data[str(date[2])]:
            curr_month_days = current_month_days(month, date[2])
            for day in range(day_number, max(curr_month_days) + 1):
                for line in range(1, bath.line_amount() + 1):
                    for hours in range(hour, bath.closing_hour()):
                        availability = data[str(date[2])][month][str(day)][str(line)][str(hour)]
                        if availability != 0:
                            return date_description((day, int(month), date[2]), hours, reservation_length, line)
                        if hours == bath.closing_hour() - 1:
                            break
                hour = bath.opening_hour()
            day_number = 1
    else:
        for month in data[str(date[2])]:
            curr_month_days = current_month_days(month, date[2])
            for day in range(day_number, max(curr_month_days) + 1):
                for hours in range(hour, bath.closing_hour()):
                    if hours == bath.closing_hour():
                        break
                    availability = availability_check_clients(data[str(date[2])][month][str(day)], reservation_length, bath, hour)
                    if availability[0]:
                        line = availability[2]
                        return date_description((int(day), int(month), date[2]), min(availability[1]), reservation_length, line)
                hour = bath.opening_hour()
            day_number = 1


def suggest_for_groups(data, reservation_length, bath):
    """
    data - reservation history
    w trakcie pracy
    """
    date, hour = get_date_and_hour(bath)
    day_number = date[0]
    if reservation_length == 1:
        for month in data[str(date[2])]:
            curr_month_days = current_month_days(month, date[2])
            for day in range(day_number, max(curr_month_days) + 1):
                for line in range(1, bath.line_amount() + 1):
                    for hours in range(hour, bath.closing_hour()):
                        if group_amount_check(data[str(date[2])][month][str(day)], hour, bath):
                            availability = data[str(date[2])][month][str(day)][str(line)][str(hour)]
                            if availability == 5:
                                return date_description((day, int(month), date[2]), hours, reservation_length, line)
                            if hours == bath.closing_hour() - 1:
                                break
                hour = bath.opening_hour()
            day_number = 1
    else:
        for month in data[str(date[2])]:
            curr_month_days = current_month_days(month, date[2])
            for day in range(day_number, max(curr_month_days) + 1):
                for hours in range(hour, bath.closing_hour()):
                    if hours == bath.closing_hour():
                        break
                    availability = availability_check_groups(data[str(date[2])][month][str(day)], reservation_length, bath, hour)
                    if availability[0]:
                        line = availability[2]
                        return date_description((day, int(month), date[2]), min(availability[1]), reservation_length, line)
                hour = bath.opening_hour()
            day_number = 1
