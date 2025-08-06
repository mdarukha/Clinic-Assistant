# function to classify user query and return a route based on keywords
def classify_query(query):
    q = query.lower()

    # different tool-based keyword lists
    insurance_keywords = ["insurance", "covered", "accept", "coverage", "plan", "network"]
    if any(word in q for word in insurance_keywords):
        return "insurance"

    hours_keywords = ["open", "hours", "time", "when are you open", "what time", "business hours"]
    if any(word in q for word in hours_keywords):
        return "hours"

    calendar_keywords = ["appointment", "book", "schedule", "available", "availability", "can i come in", "next open", "see someone"]
    if any(word in q for word in calendar_keywords):
        return "calendar"

    med_keywords = [
        "symptom", "treatment", "diagnosis", "disease", "pain", "cough", "fever", "flu",
        "diabetes", "cancer", "asthma", "rash", "hypertension", "cholesterol", "injury", "infection"
    ]
    if any(term in q for term in med_keywords):
        return "medical"

    # defaults to clinic-related questions
    return "clinic"