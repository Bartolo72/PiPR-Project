from flask_login import current_user
from flaskblog.__init__ import database
from day_data import Day_data
from datetime import datetime


def calculateTime(sleepStart, deadline):
    username = current_user.username
    database.load_from_file()
    for person in database.people:
        if person.username == username:
            phaze = person.phaze
            person.sleptFlag = 1
            break
    hourStart = int(sleepStart.hour)
    hourStop = int(deadline.hour)
    minStart = int(sleepStart.minute)
    minStop = int(deadline.minute)
    stop = 60 * hourStop + minStop
    start = 60 * hourStart + minStart
    if stop < start:
        stop += 1440
    hours = (start + ((stop - start) // phaze) * phaze) // 60
    minutes = (start + ((stop - start) // phaze) * phaze) % 60
    hours %= 24
    sug_wake_up = f'{hours:02}:{minutes:02}'
    for person in database.people:
        if person.username == username:
            person.sleptFlag = 1
            beg_of_sleep = f'{hourStart:02}:{minStart:02}'
            date = datetime.now().strftime('%d-%m-%Y')
            new_data = Day_data(beg_of_sleep, sug_wake_up, date, False)
            person.add_day_data(new_data)
            break
    database.save_to_file(database.people)
    return sug_wake_up

def calculatePhaze(sleepStart, sleepend):
    username = current_user.username
    database.load_from_file()
    for person in database.people:
        if person.username == username:
            THEuser = person
    hourStart = int(sleepStart.hour)
    hourStop = int(sleepend.hour)
    minStart = int(sleepStart.minute)
    minStop = int(sleepend.minute)
    stop = 60 * hourStop + minStop
    start = 60 * hourStart + minStart
    if stop < start:
        stop += 1440
    phaze = (stop - start) // 5
    THEuser.phaze = phaze
    database.save_to_file(database.people)
    return phaze
