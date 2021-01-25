import json
from person import Person
from day_data import Day_data


class DataBase:
    def __init__(self, path):
        self.people = []
        self.path = path

    def load_from_file(self):
        with open(self.path, 'r') as filehandle:
            self.people = []
            self.people = read_from_json(filehandle)

    def save_to_file(self, people):
        with open(self.path, 'w') as filehandle:
            write_to_json(filehandle, people)


def read_from_json(filehandle):
    people = []
    data = json.load(filehandle)
    for item in data:
        username = item['username']
        phaze = item['phaze']
        sleptFlag = item['sleptFlag']
        userdata = item['userdata']
        person = Person(username, phaze, sleptFlag, [])
        for day_data in userdata:
            sleepStart = day_data['sleepStart']
            sleepEnd = day_data['sleepEnd']
            date = day_data['date']
            confirmed = day_data['confirmed']
            read_data = Day_data(sleepStart, sleepEnd, date, confirmed)
            person.add_day_data(read_data)
        people.append(person)
    return people


def write_to_json(filehandle, people):
    data = []
    for person in people:
        username = person.username
        phaze = person.phaze
        sleptFlag = person.sleptFlag
        userdata = []
        for slp_data in person.data:
            day_data = {
                'sleepStart': slp_data.sleepStart,
                'sleepEnd': slp_data.sleepEnd,
                'date': slp_data.date,
                'confirmed': slp_data.confirmed
            }
            userdata.append(day_data)
        pers_data = {
            'username': username,
            'phaze': phaze,
            'sleptFlag': sleptFlag,
            'userdata': userdata,
        }
        data.append(pers_data)
    json.dump(data, filehandle)
