from datetime import datetime


class Branch:
    def __init__(self, number: int, name: str, suburb: str, phone_number: str):
        self.number = number
        self.name = name
        self.suburb = suburb
        self.phone_number = phone_number
        self.is_open = False

    def open(self):
        self.is_open = True
        print(f'{self.name} is open as of {datetime.now()}')
        return

    def close(self):
        self.is_open = False
        print(f'{self.name} is closed as of {datetime.now()}')
        return

    def update_phone_number(self, new_number: str):
        old_number = self.phone_number
        self.phone_number = new_number
        print(
            f'Phone number is updated successfully: {old_number} -> {self.phone_number} as of {datetime.now()}')
        return
