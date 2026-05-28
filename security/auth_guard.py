import streamlit as st

# =====================================================
# REQUIRE LOGIN
# =====================================================

def require_login():

    if not st.session_state.get(

        "vault_unlocked",

        False
    ):

        st.warning(
            "🔒 Please unlock the vault first."
        )

        st.switch_page(
            "Dashboard.py"
        )

        st.stop()