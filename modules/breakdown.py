def generate_breakdown(users):

    colour_breakdown = {}
    gender_breakdown = {"male": 0, "female": 0}
    age_breakdown = {
        (0, 9): 0,
        (10, 19): 0,
        (20, 29): 0,
        (30, 39): 0,
        (40, 49): 0,
        (50, 59): 0,
        (60, 69): 0,
        (70, 79): 0,
        (80, 89): 0,
        (90, 99): 0,
        (100,): 0,
    }
    domain_breakdown = {}
    county_breakdown = {}
    breakdown = {
        "colour breakdown": colour_breakdown,
        "gender breakdown": gender_breakdown,
        "age breakdown": age_breakdown,
        "domain breakdown": domain_breakdown,
        "county breakdown": county_breakdown,
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

        for group in age_breakdown.keys():
            if user["age"] >= group[0] and (
                len(group) == 1 or user["age"] < group[1]
            ):
                age_breakdown[group] += 1
                break
        domain = (user["email"].split("@"))[-1]
        if domain in domain_breakdown:
            domain_breakdown[domain] += 1
        else:
            domain_breakdown[domain] = 1

        if user["county"] in county_breakdown:
            county_breakdown[user["county"]] += 1
        else:
            county_breakdown[user["county"]] = 1

    return breakdown

