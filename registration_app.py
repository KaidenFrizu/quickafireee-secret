import streamlit as st
import os
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="osu!Quickfire Registration",
                   page_icon=":fire:", initial_sidebar_state="collapsed")

# HACK: This is to get rid of the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# To check if we're using this for a LAN party
st.session_state["CONQUEST_MODE"] = os.environ.get("CONQUEST_MODE", False)

# PAGE SETUP ENDS HERE


def create_authorization_url(client_id, redirect_uri, scope):
    """ Returns the authorization URL for the osu! API"""
    return f"https://osu.ppy.sh/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"


@st.cache_data
def retrieve_token(client_id, client_secret, code, redirect_uri):
    """ Retrieves a token derived from the code sent by the osu! API """
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code[0],
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    res = requests.post("https://osu.ppy.sh/oauth/token", data=data)
    assert res.status_code == 200
    return res.json()["access_token"]


@st.cache_data
def get_user_data(token):
    """ Returns the user data from the osu! API """
    res = requests.get("https://osu.ppy.sh/api/v2/me/osu", timeout=2048, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    })

    return res.json()


auth_code = st.experimental_get_query_params().get("code")
client_id = os.environ.get("CLIENT_ID", 7270)
client_secret = os.environ.get("CLIENT_SECRET", None)
redirect_uri = os.environ.get("REDIRECT_URI", "http://127.0.0.1:8501/")
scope = "identify"
auth_url = create_authorization_url(client_id, redirect_uri, scope)

# We technically don't need this but just in case someone tries to hotlink this page, they have to go through OAuth.
if auth_code:
    access_token = None

    if access_token:
        data = get_user_data(access_token)
        st.session_state.osu_user_id = data["id"]
        st.session_state.osu_username = data["username"]
    else:
        access_token = retrieve_token(
            client_id, client_secret, auth_code, redirect_uri)
        data = get_user_data(access_token)
        st.session_state.osu_user_id = data["id"]
        st.session_state.osu_username = data["username"]

    with open("REGISTRATION_INTRO.md", encoding="utf-8") as f:
        st.markdown(f.read(), unsafe_allow_html=True)

    if st.button("Continue"):
        switch_page("register")  # type:ignore
else:
    st.markdown("# osu!Quickfire Registration")
    st.write(
        f"Please authorize this app to use your osu! account by clicking [here]({auth_url})")
    st.write("You will be redirected to a page where you can authorize this app to access your osu! account.")
    st.write("Once you have authorized this app, you will be redirected back to this page. Please click the button below to continue.")
