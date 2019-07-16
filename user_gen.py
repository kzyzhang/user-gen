from faker import Faker
import datetime
import re
import sys

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


def user_gen(no_users):
    users = []

    for user in range(no_users):

        DOB = fake.date_of_birth(minimum_age=0, maximum_age=115)
        DOB_str = DOB.strftime("%d-%m-%Y")
        user = {
            "name": fake.name(),
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
