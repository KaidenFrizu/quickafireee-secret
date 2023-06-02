import streamlit as st

service_acct_creds = {
    'type': st.secrets.GSheets.type,
    'project_id': st.secrets.GSheets.project_id,
    'private_key_id': st.secrets.GSheets.private_key_id,
    'private_key': st.secrets.GSheets.private_key,
    'client_email': st.secrets.GSheets.client_email,
    'client_id': st.secrets.GSheets.client_id,
    'auth_uri': st.secrets.GSheets.auth_uri,
    'token_uri': st.secrets.GSheets.token_uri,
    'auth_provider_x509_cert_url': st.secrets.GSheets.auth_provider_x509_cert_url,
    'client_x509_cert_url': st.secrets.GSheets.client_x509_cert_url
}
