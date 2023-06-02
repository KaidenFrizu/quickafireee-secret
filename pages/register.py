import streamlit as st
import pandas as pd
from sheet_manager import sheet_manager
from sheet_manager import servsecrets
from sheet_manager import generator

st.set_page_config(page_title="osu!Quickfire Registration",
    page_icon=":fire:", initial_sidebar_state="collapsed")

# HACK: This is to get rid of the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

with open("REGISTRATION_HEADER.md", encoding="utf-8") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

with st.form("registration_form"):
    osu_username = st.text_input("osu!username", st.session_state.get("osu_username", ""), 24)
    email = st.text_input("Email", "", 24)
    osu_url = st.text_input("osu!profile URL", f"https://osu.ppy.sh/users/{st.session_state.get('osu_user_id', '')}")
    # Since we may have some LAN tournaments, we can just toggle this and restart the application
    # Since we *might* reuse this beyond CONQUEST 2023
    if st.session_state["CONQUEST_MODE"]:
        conquest_proof = st.text_input("Proof of Attendance (Must be a Google Drive Link)", "")
        days_attending = st.multiselect("Days Attending", ["Day 1", "Day 2", "Day 3", "All Days"])
        phone_number = st.text_input("Phone Number", "")
    has_contented = st.checkbox(
        "I consent to the collection of my data as per provisions of the Data Privacy Act of 2012.")

    if st.form_submit_button("Submit"):
        if not has_contented:
            st.error("You must consent to the collection of your data.")
        else:
            # Google forms logic goes here
            manager = sheet_manager.SheetManager(
                creds = servsecrets.service_acct_creds,
                sheets_key = st.secrets.GSheets.sheets_key
            )

            data_dict = {
                'date_created':[generator.generate_current_time()],
                'email':[email],
                'osu_username':[osu_username],
                'days_attending':[days_attending],
                'has_consented':True
            }

            data_dict['reg_id'] = generator.generate_reg_id(
                str_input = ''.join(
                    [
                        data_dict['date_created'],
                        email,
                        osu_username,
                        days_attending
                    ]
                )
            )

            manager.push_data(sheet_number=0, data=pd.DataFrame(data_dict))
            st.success("Thank you for registering! The tournament staff will get in touch with you soon.")

