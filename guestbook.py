import os
import re
import datetime
import streamlit as st
import pandas as pd
import requests
from sheet_manager import sheet_manager
from sheet_manager import servsecrets
from sheet_manager import generator


def post_to_webhook(message):
    url = os.environ.get("WEBHOOK_URL", "https://example.com") or "https://example.com"
    data = {"content": message}
    params = {"thread_id": os.environ.get("WEBHOOK_THREAD_ID", "0") or "0"}
    result = requests.post(url, json=data, params=params, timeout=2048)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return Exception(err)
    else:
        print(f'Payload delivered successfully, code {result.status_code}.')


st.set_page_config(page_title="osu! booth Guestbook",
                   page_icon=":heart:", initial_sidebar_state="collapsed")

# HACK: This is to get rid of the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Get header
with open("GUESTBOOK_HEADER.md", "r", encoding="utf-8") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# Begin Guestbook Entrypoint

name = st.text_input("Please enter your nickname")
is_osu_player = st.checkbox("Do you have an existing osu account?")
ign = ''

if is_osu_player:
    ign = st.text_input("Please enter you osu ingame name here")
    
email = st.text_input("Please enter your email.")
button = st.button('Submit')

if button:
    if len(name) <= 0:
        st.warning("Please enter your name.")
    elif (0 == len(ign) or len(ign) > 21) and is_osu_player:
        st.warning("Please enter your osu! ingame name.")
    elif re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email) is None:
        st.warning("Please enter a valid email.")
    else:
        manager = sheet_manager.SheetManager(
            creds=servsecrets.service_acct_creds,
            sheets_key=st.secrets.GSheets.guestbook_sheets_key
        )

        data_dict = {
            'timestamp': [generator.generate_current_time()],
            'name': [name],
            'is_osu_user': [is_osu_player],
            'osu_username': [ign],
            'email': [email],
        }

        # The sheets must have 4 column names (as per keys in data_dict)
        # that was made before pushing
        manager.push_data(sheet_number=0, data=pd.DataFrame(data_dict))
        st.success(f'Thanks for signing to the Guestbook, {name}!')  

# End Guestbook Entrypoint