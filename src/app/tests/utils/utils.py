import random
import string
from datetime import datetime, timedelta


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def generate_random_date():
    start_date_obj = datetime.strptime("2000-01-01", "%Y-%m-%d")
    end_date_obj = datetime.strptime("2023-07-07", "%Y-%m-%d")

    time_delta = end_date_obj - start_date_obj
    random_days = random.randint(0, time_delta.days)
    random_date = start_date_obj + timedelta(days=random_days)
    return random_date


def generate_random_amount(max_value=999999, decimals=2):
    random_integer = random.randint(0, int(max_value * 10**decimals))
    random_amount = random_integer / 10**decimals
    return random_amount


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
