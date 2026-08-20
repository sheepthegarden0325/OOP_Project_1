from datetime import datetime
from bank import Bank


class Branch:
    __next_number = 1

    def __init__(self, name: str, suburb: str, phone_number: str):
        self.__number = Branch.__next_number
        Branch.__next_number += 1
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = None
        if isinstance(suburb, str):
            self.__suburb = suburb
        else:
            self.__suburb = None
        if isinstance(phone_number, str):
            self.__phone_number = phone_number
        else:
            self.__phone_number = None
        self.__is_open = False
        Bank.add_branch(self)

    def open(self):
        self.__is_open = True
        print(f'{self.__name} is open as of {datetime.now()}')
        return

    def close(self):
        self.__is_open = False
        print(f'{self.__name} is closed as of {datetime.now()}')
        return

    def set_phone_number(self, new_number: str):
        if isinstance(new_number, str):
            old_number = self.__phone_number
            self.__phone_number = new_number
            print(
                f'Phone number is updated successfully: {old_number} -> {self.__phone_number} as of {datetime.now()}')

    def get_number(self):
        return self.__number
