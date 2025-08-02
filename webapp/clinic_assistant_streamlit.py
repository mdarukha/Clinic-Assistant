import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from router.query_router import classify_query
from retriever.retrieve import retrieve_top_k
from tools.hours_checker import check_hours
from tools.insurance_checker import check_insurance
from tools.calendar_checker_streamlit import check_and_book_appointment  # streamlit version with status messages
from llm.generator import generate_response

# similar to clinic_assistant_cli to be used with CLI but modified calendar to accept multiple info fields for streamlit integration

def handle_query(query, name=None, email=None, confirm=None):
    route = classify_query(query)

    if route == "insurance":
        return check_insurance(query)

    elif route == "hours":
        return check_hours(query)

    elif route == "calendar":
        return check_and_book_appointment(query, name=name, email=email, confirm=confirm)

    elif route == "clinic":
        context = retrieve_top_k(query, "models/clinic_faq.index", "models/clinic_faq_corpus.pkl")[0]
        return generate_response(query, context)

    elif route == "medical":
        context = retrieve_top_k(query, "models/pubmed.index", "models/pubmed_corpus.pkl")[0]
        return generate_response(query, context)

    else:
        return "Sorry, I couldn't understand your question."