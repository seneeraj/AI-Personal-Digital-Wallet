import streamlit as st

from security.master_auth import (
    change_master_password
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Settings",

    page_icon="⚙️",

    layout="centered"
)

# =====================================================
# TITLE
# =====================================================

st.title("⚙️ Settings")

st.divider()

# =====================================================
# CHANGE PASSWORD
# =====================================================

st.subheader("🔐 Change Master Password")

current_password = st.text_input(

    "Current Password",

    type="password"
)

new_password = st.text_input(

    "New Password",

    type="password"
)

confirm_password = st.text_input(

    "Confirm New Password",

    type="password"
)

# =====================================================
# UPDATE BUTTON
# =====================================================

if st.button("🔄 Update Password"):

    # =============================================
    # VALIDATION
    # =============================================

    if not current_password:

        st.error(
            "Enter current password."
        )

    elif not new_password:

        st.error(
            "Enter new password."
        )

    elif new_password != confirm_password:

        st.error(
            "New passwords do not match."
        )

    else:

        success, message = (

            change_master_password(

                current_password,

                new_password
            )
        )

        if success:

            st.success(message)

        else:

            st.error(message)