import re

phone_book = {}
exit_commands = ["good bye", "close", "exit"]
is_bot_running = False


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            if type(e.args[0]) is dict and 'message' in e.args[0]:
                return e.args[0]['message']
            else:
                return "Contact does not exist."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Invalid input."

    return inner


def stop_execution(func):
    def inner(*args, **kwargs):
        global is_bot_running
        is_bot_running = False
        return func(*args, **kwargs)

    return inner


def greeting():
    return "How can I help you?"


@input_error
def add_contact(*args):
    name = " ".join(args[:-1])
    phone_number = args[-1]
    if phone_book.get(name) is not None:
        raise KeyError({
            "message": f'User with name "{name}" already exists. In order to update phone number use "change.." command'
        })
    if not str.isnumeric(phone_number):
        raise ValueError
    phone_book[name] = phone_number
    return f'Added {name} {phone_number}'


@input_error
def change_contact(*args):
    name = " ".join(args[:-1])
    prev_phone_number = phone_book[name]
    phone_number = args[-1]
    if not str.isnumeric(phone_number):
        raise ValueError
    phone_book[name] = phone_number
    return f'Phone number has been changed from "{prev_phone_number}" to "{phone_number}" for the user "{name}"'


@input_error
def get_contact_by_name(*args):
    name = " ".join(args)
    phone_number = phone_book[name]
    return phone_number


def get_all_contacts():
    return '\n'.join(map(lambda k: f'{k} {phone_book[k]}', phone_book.keys()))


def command_parser(user_input):
    [command, *command_arguments] = re.split(r'\s+', user_input)
    command = command.lower()
    if command in exit_commands:
        output = say_goodbye()
    elif command == "hello":
        output = greeting()
    elif command == "add":
        output = add_contact(*command_arguments)
    elif command == 'phone':
        output = get_contact_by_name(*command_arguments)
    elif command == 'change':
        output = change_contact(*command_arguments)
    elif user_input.lower().startswith('show all'):
        output = get_all_contacts()
    else:
        output = "Sorry, the command you entered was not recognized"

    return output


@stop_execution
def say_goodbye():
    return "Good bye!"


def main():
    global is_bot_running
    is_bot_running = True
    while is_bot_running:
        print(
            'Available commands: "hello", "add ...", "change ...", "phone ...", "show all", "good bye", "close", "exit"'
        )
        print(command_parser(input("Enter Command: ")))


if __name__ == '__main__':
    main()
