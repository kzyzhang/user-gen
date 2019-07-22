import datetime
import requests
import urllib.request
import re
from faker import Faker
from modules.cat_status_codes import cat_http_code

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
        # print(name_response, name, gender)
    return gender


def gen_first_name(name):
    """get the first name of a user from their full name
    
    Arguments:
        name {str} -- full name    
    Return:
        str -- first name
    
    """
    name_split = name.split(" ")
    if len(name_split) == 2:
        first_name = name_split[0]
    else:
        first_name = name_split[1]

    return first_name


def random_postcode_generator():
    url = "https://www.doogal.co.uk/CreateRandomPostcode.ashx"
    response = requests.get(url)
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
    response = requests.get(url)
    county = (response.text).split("\t")[8]
    if len(county) == 0:
        county = f"N\A"
    return county


def user_gen(no_users):
    users = []

    for user in range(no_users):

        DOB = fake.date_of_birth(minimum_age=0, maximum_age=115)
        DOB_str = DOB.strftime("%d-%m-%Y")
        name = fake.name()
        postcode = random_postcode_generator()

        user = {
            "name": name,
            "gender": estimate_gender(name),
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

