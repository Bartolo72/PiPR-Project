from day_data import Day_data


class Person():
    def __init__(self, username, phaze=100, sleptFlag=0, userdata=[]):
        self.username = username
        self.phaze = phaze
        self.sleptFlag = sleptFlag
        self.data = userdata

    def set_phaze(self, new_phaze: int):
        self.phaze = new_phaze

    def set_sleptFlag(self, new_flag):
        self.sleptFlag = new_flag

    def add_day_data(self, new_data:'Day_data'):
        self.data.append(new_data)
