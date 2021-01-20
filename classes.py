import datetime
from calendar import Calendar


class NotEnoughWeekDays(Exception):
    def __init__(self, week_days):
        super().__init__("Not enough week days in this list - should be 7")
        self.week_days = week_days


class InvalidHour(Exception):
    def __init__(self):
        super().__init__("Hour must be in range 0-23")


class InvalidMonth(Exception):
    def __init__(self):
        super().__init__("Month not are in range 1-12")


class InvalidYear(Exception):
    def __init__(self):
        super().__init__("This year was in the past")


class InvalidDay(Exception):
    def __init__(self):
        super().__init__("Day number is not in current month")


class Bath:
    def __init__(self, name, line_amount, opening_hour, closing_hour):
        self._name = name
        self._line_amount = line_amount
        if opening_hour not in range(0, 24):
            raise InvalidHour()
        self._opening_hour = opening_hour
        if closing_hour not in range(0, 24):
            raise InvalidHour()
        self._closing_hour = closing_hour

    def name(self):
        return self._name

    def line_amount(self):
        return self._line_amount

    def opening_hour(self):
        return self._opening_hour

    def closing_hour(self):
        return self._closing_hour


class IndividualType:
    def __init__(self, price, name='normal'):
        self.price = price
        self.name = name

    def set_price(self, new_price):
        self.price = new_price


class Individual:
    def __init__(self, types):
        """
        types - list of IndividualType objects
        self.types will be a dict {type.name:}
        """
        self.types = types

    def types_with_prices(self):
        data = {}
        for element in self.types:
            data[element.name] = element.price
        return data


class Group:
    def __init__(self, name, price):
        self.price = price
        self.name = name

    def set_price(self, new_price):
        self.price = new_price


class Clients:
    def __init__(self, individual, groups):
        """
        individual - object, contains types of individual clients and prices for hour
        groups - object, contains name and prices for hour
        """
        self.individual = individual
        self.groups = groups


class DayPart:
    def __init__(self, clients, bath, name='normal', part_opening_hour=None, part_closing_hour=None):
        self.clients = clients
        if part_opening_hour is None:
            self.part_opening_hour = bath.opening_hour()
        elif part_opening_hour not in range(0, 24):
            raise InvalidHour()
        else:
            self.part_opening_hour = part_opening_hour
        if part_closing_hour is None:
            self.part_closing_hour = bath.closing_hour()
        elif part_closing_hour not in range(0, 24):
            raise InvalidHour()
        else:
            self.part_closing_hour = part_closing_hour
        self.name = name
        self.bath = bath


class WeekDay:
    def __init__(self, day_parts, name):
        """
        day_parts - list which contains opening, closing hour of day part and price for one hour
        we assume for now that day_parts list is perfect
        """
        self.day_parts = day_parts
        self.name = name


class PriceSchedule:
    def __init__(self, week_days):
        """
        week days - lists of all week days, where each is a WeekDay object and contains day parts and prices for
        one hour at those day parts
        """
        if len(week_days) != 7:
            raise NotEnoughWeekDays()
        self.week_days = week_days


class Date:
    def __init__(self, day, month=None, year=None):
        if month is None:
            month = datetime.datetime.now().month
        elif int(month) not in range(0, 13):
            raise InvalidMonth()
        self.month = int(month)
        if year is None:
            year = datetime.datetime.now().year
        elif int(year) < datetime.datetime.now().year:
            raise InvalidYear()
        self.year = int(year)
        calendar = Calendar()
        month_days = [int(day) for day in calendar.itermonthdays(self.year, self.month)]
        if int(day) not in range(1, max(month_days)):
            raise InvalidDay()
        self.day = int(day)
