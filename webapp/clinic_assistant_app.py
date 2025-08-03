import streamlit as st
from clinic_assistant_streamlit import handle_query
import json
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# use credentials.json from streamlit secrets
if "GOOGLE_CREDENTIALS" in st.secrets and not os.path.exists("credentials.json"):
    credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    with open("credentials.json", "w") as f:
        json.dump(credentials_dict, f)

# app setup
st.set_page_config(page_title="Clinic Assistant", page_icon="🩺")
st.title("🩺 Clinic Assistant")
st.markdown("Ask a question about clinic services, hours, insurance, appointments, or general medical info.")

# initialize session state variables
for key in ["step", "name", "email", "confirm", "response", "booked"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# input field for user query
query = st.text_input("Enter your question:", key="query_input")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.booked = False
        result = handle_query(query)

        # handles calendar info flow
        if isinstance(result, dict):
            st.session_state.response = result

            if result["status"] == "need_name":
                st.session_state.step = "name"

            elif result["status"] == "need_email":
                st.session_state.step = "email"

            elif result["status"] == "need_confirm":
                st.session_state.step = "confirm"

            elif result["status"] == "done":
                if not st.session_state.booked:
                    st.success(result["message"])
                    st.session_state.booked = True
                    st.session_state.step = ""
                    st.session_state.name = ""
                    st.session_state.email = ""
                    st.session_state.confirm = ""
        else:
            st.success("**Assistant:**")
            st.write(result)

# specific streamlit flow for calendar routed questions: sequential input of patient info to confirm appt booking
if st.session_state.step == "name":
    st.session_state.name = st.text_input("👤 Please enter your full name:", key="name_input")
    if st.button("Next: Enter Email"):
        if st.session_state.name.strip():
            result = handle_query(
                st.session_state.query_input,
                name=st.session_state.name
            )
            st.session_state.response = result
            st.session_state.step = "email"
            st.rerun()

elif st.session_state.step == "email":
    st.session_state.email = st.text_input("📧 Enter your email address:", key="email_input")
    if st.button("Next: Confirm Booking"):
        if st.session_state.email.strip():
            result = handle_query(
                st.session_state.query_input,
                name=st.session_state.name,
                email=st.session_state.email
            )
            st.session_state.response = result
            st.session_state.step = "confirm"
            st.rerun()

elif st.session_state.step == "confirm":
    st.session_state.confirm = st.text_input("✅ Type 'confirm' to book your appointment:", key="confirm_input")
    if st.button("Finalize Booking"):
        if st.session_state.confirm.strip().lower() == "confirm":
            result = handle_query(
                st.session_state.query_input,
                name=st.session_state.name,
                email=st.session_state.email,
                confirm="confirm"
            )
            # show booking confirmation
            if isinstance(result, dict) and result.get("status") == "done":
                st.success(result["message"]) 
                st.session_state.booked = True
                st.session_state.step = ""
                st.session_state.name = ""
                st.session_state.email = ""
                st.session_state.confirm = ""
            else:
                st.warning("Something went wrong with booking. Please try again.")
            
