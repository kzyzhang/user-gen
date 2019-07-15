from faker import Faker
import datetime
import random
import re
import sys

date = datetime.datetime.now()
fake = Faker("en_GB")

# user = {
#     "username": "",
#     "name": "",
#     "age": "",
#     "DOB": "",
#     "favourite colour": "",
#     "address": "",
#     "postcode": "",
#     "email": "",
#     "phone number": "",
# }
# print(user)


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
    p = re.compile("^[0-9]+$")
    # return p.match(str(no_users))
    if p.match(str(no_users)) != None:

        for v in range(int(no_users)):

            DOB = fake.date_of_birth(
                tzinfo=None, minimum_age=0, maximum_age=115
            )
            DOB_str = DOB.strftime("%d-%m-%Y")
            user = {
                "name": fake.name(),
                "birthday": DOB_str,
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

    else:
        return "this is an invalid number of users"


# print(user_gen("2ef"))
if __name__ == "__main__":
    # print(sys.argv[1])
    user_lst = user_gen((sys.argv[1]))
    print(user_lst)
# DOB = fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)
# print(type(DOB))
#   fake.user_name(*args, **kwargs)

