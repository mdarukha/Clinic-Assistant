import json

# tool to repsond to questions based on clinic insurance policies using json of accepted/not accepted plans

INS_FILE = "data/insurance_rules.json"

def load_rules():
    with open(INS_FILE, "r") as f:
        return json.load(f)

# check if plan accepted or not, ppo or hmo if listed, and generate response based on clinic policy
def check_insurance(query):
    rules = load_rules()
    query = query.lower()

    accepted = [x.lower() for x in rules["accepted"]]
    not_accepted = [x.lower() for x in rules["not_accepted"]]

    for plan in accepted:
        if plan in query:
            if "hmo" in query:
                return f"{plan.title()} is accepted, but please contact the clinic to verify your HMO plan. {rules['hmo_note']}"
            return f"{plan.title()} is accepted. {rules['ppo_note']}"

    for plan in not_accepted:
        if plan in query:
            return f"Unfortunately, we do not accept {plan.title()}."

    return rules["unlisted_response"]