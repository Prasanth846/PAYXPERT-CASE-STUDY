from datetime import date

class Employee:
    def __init__(self, employee_id=None, first_name=None, last_name=None, date_of_birth=None,
                 gender=None, email=None, phone_number=None, address=None,
                 position=None, joining_date=None, termination_date=None):
        self.__employee_id = employee_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__date_of_birth = date_of_birth
        self.__gender = gender
        self.__email = email
        self.__phone_number = phone_number
        self.__address = address
        self.__position = position
        self.__joining_date = joining_date
        self.__termination_date = termination_date

    # Getters and setters
    def get_employee_id(self):
        return self.__employee_id
    def set_employee_id(self, value):
        self.__employee_id = value

    def get_first_name(self):
        return self.__first_name
    def set_first_name(self, value):
        self.__first_name = value

    def get_last_name(self):
        return self.__last_name
    def set_last_name(self, value):
        self.__last_name = value

    def get_date_of_birth(self):
        return self.__date_of_birth
    def set_date_of_birth(self, value):
        self.__date_of_birth = value

    def get_gender(self):
        return self.__gender
    def set_gender(self, value):
        self.__gender = value

    def get_email(self):
        return self.__email
    def set_email(self, value):
        self.__email = value

    def get_phone_number(self):
        return self.__phone_number
    def set_phone_number(self, value):
        self.__phone_number = value

    def get_address(self):
        return self.__address
    def set_address(self, value):
        self.__address = value

    def get_position(self):
        return self.__position
    def set_position(self, value):
        self.__position = value

    def get_joining_date(self):
        return self.__joining_date
    def set_joining_date(self, value):
        self.__joining_date = value

    def get_termination_date(self):
        return self.__termination_date
    def set_termination_date(self, value):
        self.__termination_date = value

    # Method
    def calculate_age(self):
        if self.__date_of_birth:
            today = date.today()
            return today.year - self.__date_of_birth.year - (
                (today.month, today.day) < (self.__date_of_birth.month, self.__date_of_birth.day))
        return None
