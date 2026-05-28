import streamlit as st

def initialize_session():

    if "vault_unlocked" not in st.session_state:
        st.session_state["vault_unlocked"] = False

def unlock_vault():

    st.session_state["vault_unlocked"] = True

def lock_vault():

    st.session_state["vault_unlocked"] = False

def is_vault_unlocked():

    return st.session_state["vault_unlocked"]