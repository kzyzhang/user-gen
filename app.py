from faker import Faker
import datetime
import sys
import re
import requests
import urllib.request
import cv2
import numpy as np
import bs4 as bs

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
        name_request = requests.get(
            "https://api.genderize.io/?name=" + first_name
        )

        if name_request.status_code != 200:

            image = cat_http_code(name_request.status_code)
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            sys.exit(1)

        name_data = name_request.json()
        gender = name_data["gender"]
        print(name_request, name, gender)
    return gender


def cat_http_code(status_code):
    root_url = "https://http.cat/"
    url = root_url + str(status_code)
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


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


def generate_breakdown(users):

    colour_breakdown = {}
    gender_breakdown = {"male": 0, "female": 0}
    age_breakdown = {}
    domain_breakdown = {}
    breakdown = {
        "colour breakdown": colour_breakdown,
        "gender breakdown": gender_breakdown,
        "age breakdown": age_breakdown,
        "domain breakdown": domain_breakdown,
    }
    for user in users:

        if user["favourite colour"] in colour_breakdown:
            colour_breakdown[user["favourite colour"]] += 1
        else:
            colour_breakdown[user["favourite colour"]] = 1

        if user["gender"] == "female":
            gender_breakdown["female"] += 1
        else:
            gender_breakdown["male"] += 1

        for group in age_ranges:
            if user["age"] >= group[0] and (
                len(group) == 1 or user["age"] < group[1]
            ):
                age_breakdown[group] = user["age"]
                break
        domain = (user["email"].split("@"))[-1]
        # print(user["email"], domain)

        if domain in domain_breakdown:
            domain_breakdown[domain] += 1
        else:
            domain_breakdown[domain] = 1

    return breakdown


age_ranges = [
    (0, 9),
    (10, 19),
    (20, 29),
    (30, 39),
    (40, 49),
    (50, 59),
    (60, 69),
    (70, 79),
    (80, 89),
    (90, 99),
    (100,),
]


if __name__ == "__main__":
    input = sys.argv[1]
    validate_input(input)
    quantity = int(input)

    users = user_gen(quantity)
    user_gen(quantity)
    print(users)
    print(generate_breakdown(users))
