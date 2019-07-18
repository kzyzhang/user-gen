from faker import Faker
import datetime
import sys
import re
import requests
import numpy as np
import urllib.request
import cv2


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
        url = "https://api.genderize.io/?name=" + first_name
        name_response = requests.get(url)
        # name_response.status_code = 444

        cat_http_code(name_response.status_code, url)

        name_data = name_response.json()
        gender = name_data["gender"]
        print(name_response, name, gender)
    return gender


def random_postcode_generator():
    url = "https://www.doogal.co.uk/CreateRandomPostcode.ashx"
    response = requests.post(url)
    postcode = (response.text).split(",")[0]
    return postcode


def find_county_from_postcode(postcode):
    postcode_split = postcode.split(" ")
    url = (
        "https://www.doogal.co.uk/GetPostcode.ashx?postcode="
        + postcode_split[0]
        + "%20"
        + postcode_split[1]
    )
    response = requests.post(url)
    response_text = response.text
    county = response_text.split("\t")[8]
    if len(county) == 0:
        county = "N\\A"
    return county


def cat_http_code(status_code, url):
    if status_code != 200:
        print(url)
        root_url = "https://http.cat/"
        cat_url = root_url + str(status_code)
        resp = urllib.request.urlopen(cat_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        sys.exit(1)
    else:
        pass


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
        gender = estimate_gender(name)
        postcode = random_postcode_generator()
        # print(user)
        user = {
            "name": name,
            "gender": gender,
            "dob": DOB_str,
            "age": age_calculate(DOB, date),
            "favourite colour": fake.color_name(),
            "address": fake.street_address(),
            "postcode": postcode,
            "county": find_county_from_postcode(postcode),
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
    # county_breakdown = {}
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

                if group in age_breakdown.keys():
                    age_breakdown[group] += 1
                else:
                    age_breakdown[group] = 1
                break

        domain = (user["email"].split("@"))[-1]
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
    print(users)
    print(generate_breakdown(users))
