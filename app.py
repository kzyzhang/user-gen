import sys
from modules.gen_user import user_gen
from modules.gen_user import validate_input
from modules.breakdown import generate_breakdown

if __name__ == "__main__":
    input = sys.argv[1]
    validate_input(input)
    quantity = int(input)
    users = user_gen(quantity)
    breakdown = generate_breakdown(users)
    for key in users:
        print(key)
    for key in breakdown:
        print(breakdown[key])

