from datetime import date, datetime, timedelta
from collections import defaultdict


WEEK_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def get_date_range():
    today: date = date.today()
    today_weekday: int = today.weekday()
    from_date: date = today - timedelta(days=2) if today_weekday == 0 else today
    to_date: date = from_date + timedelta(days=7)
    return from_date, to_date


def get_birthdays_per_week(users) -> dict:
    start_date, end_date = get_date_range()

    def resolve_birthdate(usr: dict) -> dict:
        dt = usr.get('birthday')
        year = start_date.year if (start_date.year == end_date.year) or dt.month == 12 else end_date.year
        dt = dt.replace(year=year)
        usr.update(birthday=dt)
        return usr

    res = defaultdict(list)
    for user in [resolve_birthdate(user) for user in users]:
        if start_date <= user.get('birthday') <= end_date:
            key = datetime.strftime(user.get('birthday'), '%A')
            key = key if key in WEEK_DAYS else WEEK_DAYS[0]
            res[key].append(user.get('name'))

    return dict(res)


if __name__ == "__main__":

    user_list = [
        {"name": "Jan Koum", "birthday": datetime(1976, 11, 4).date()},
    ]

    result = get_birthdays_per_week(user_list)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
