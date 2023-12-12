from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        super().__init__(value)

    @staticmethod
    def is_valid(phone_number: str):
        return len(phone_number) == 10 and phone_number.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, record: Record):
        self.data.pop(record, None)

    def find(self, name: str) -> Record:
        return self.data.get(name)
