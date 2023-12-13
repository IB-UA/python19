import re
from collections import UserDict
from datetime import datetime, date
from pathlib import Path
from pickle import dump, load
from atexit import register


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if isinstance(value, date):
            self.__value = value
        else:
            raise ValueError("Value should be a date object")


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("The string should contain only digits and its length equal 10")

    @staticmethod
    def is_valid(phone_number: str):
        return len(phone_number) == 10 and phone_number.isdigit()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday is not None:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number: str):
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is not None:
            self.phones.remove(phone)

    def edit_phone(self, old_number: str, new_number: str):
        phone = self.find_phone(old_number)
        if phone is None:
            raise ValueError
        phone.value = new_number

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        current_date: date = datetime.now().date()
        current_year: int = current_date.year
        current_year_birthday: date = self.birthday.value.replace(year=current_year)
        if current_year_birthday < current_date:
            current_year_birthday = current_year_birthday.replace(year=(current_year_birthday.year + 1))
        return (current_year_birthday - current_date).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    path = Path("addressbook.bin")
    instance = None
    restored_data = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(AddressBook, cls).__new__(cls)
            cls.instance.restored_data = cls.instance.load()
            register(cls.instance.dump)
        return cls.instance

    def __init__(self):
        super().__init__()
        if self.restored_data is not None:
            self.data.update(self.restored_data)
            self.restored_data = None

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, record: Record):
        self.data.pop(record, None)

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def iterator(self, item_number):
        counter = 0
        result = []
        for item, record in self.data.items():
            result.append(f'{item}: {record}\n')
            counter += 1
            if counter >= item_number:
                yield ''.join(result)
                counter = 0
                result = []
        return ''.join(result)

    def dump(self):
        with open(self.path, 'wb') as fw:
            dump(self.data, fw)

    def load(self):
        if not self.path.is_file():
            return None
        with open(self.path, 'rb') as fr:
            return load(fr)

    def find_by_string(self, term):
        search_result = []
        for record in self.data.values():
            for field in [record.name, *record.phones]:
                if re.search(term, field.value, re.IGNORECASE):
                    search_result.append(str(record))
                    break

        return "\n".join(search_result)
