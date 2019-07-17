from faker import Faker
import datetime
import re
import sys

import requests

date = datetime.datetime.now()
fake = Faker("en_GB")


def age_calculate(DOB, date):
    if date.month == DOB.month:
        if date.day >= DOB.day:
            return date.year - DOB.year
        else:
            return date.year - DOB.year - 1
    elif date.month > DOB.month:
        return date.year - DOB.year
    else:
        return date.year - DOB.year - 1


def estimate_gender(name):

    if "Mr" in name:
        gender = "male"

    elif "Miss " in name or "Mrs." in name or "Ms." in name:
        gender = "female"

    else:

        first_name = gen_first_name(name)
        r = requests.get("https://api.genderize.io/?name=" + first_name)
        name_data = r.json()
        gender = name_data["gender"]
        print(name, gender)
    return gender


def gen_first_name(name):
    name_split = name.split(" ")

    if len(name_split) == 2:
        first_name = name_split[0]
    else:
        first_name = name_split[1]
    return first_name


def user_gen(no_users):
    users = []

    for user in range(no_users):

        DOB = fake.date_of_birth(minimum_age=0, maximum_age=115)
        DOB_str = DOB.strftime("%d-%m-%Y")
        name = fake.name()
        user = {
            "name": name,
            "gender": estimate_gender(name),
            "dob": DOB_str,
            "age": age_calculate(DOB, date),
            "favourite colour": fake.color_name(),
            "address": fake.street_address(),
            "postcode": fake.postcode(),
            "email": fake.email(),
            "phone number": fake.phone_number(),
            "username": fake.user_name(),
        }

        users.append(user)
    return users


def validate_input(input):
    regex = re.compile("^[0-9]+$")

    if regex.match(input) is not None:
        pass
    else:
        print(f"{input} not a valid number")
        sys.exit(1)


if __name__ == "__main__":
    input = sys.argv[1]
    validate_input(input)
    quantity = int(input)
    users = user_gen(quantity)
    print(users)
