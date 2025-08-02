import argparse
from router.query_router import classify_query
from retriever.retrieve import retrieve_top_k
from tools.hours_checker import check_hours
from tools.insurance_checker import check_insurance
from tools.calendar_checker_cli import check_and_book_appointment  # version for CLI use
from llm.generator import generate_response

# file to run assistant using CLI
def main():
    print("Running clinical assistant...")
    
    # parse command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="User query to assistant")
    args = parser.parse_args()
    query = args.query

    # classify query into route and direct
    route = classify_query(query)
    print(f"[Router] Query classified as: {route}")

    # different routes
    if route == "insurance":
        answer = check_insurance(query)

    elif route == "hours":
        answer = check_hours(query)

    elif route == "calendar":
        answer = check_and_book_appointment(query)

    elif route == "clinic":
        context = retrieve_top_k(query, "models/clinic_faq.index", "models/clinic_faq_corpus.pkl")[0]
        answer = generate_response(query, context)

    elif route == "medical":
        context = retrieve_top_k(query, "models/pubmed.index", "models/pubmed_corpus.pkl")[0]
        answer = generate_response(query, context)

    else:
        answer = "Sorry, I couldn't understand your question."

    print("\nAssistant:", answer)

if __name__ == "__main__":
    main()