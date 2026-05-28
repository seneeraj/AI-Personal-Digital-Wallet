import streamlit as st
import hashlib
import os

MASTER_FILE = "security/master.hash"

# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()

# =====================================================
# SETUP MASTER PASSWORD
# =====================================================

def setup_master_password():

    st.title("🔐 Create Master Password")

    password = st.text_input(

        "Create Password",

        type="password"
    )

    confirm_password = st.text_input(

        "Confirm Password",

        type="password"
    )

    if st.button("Create Vault"):

        if not password:

            st.error(
                "Password cannot be empty."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            hashed = hash_password(
                password
            )

            os.makedirs(
                "security",
                exist_ok=True
            )

            with open(
                MASTER_FILE,
                "w"
            ) as f:

                f.write(hashed)

            st.success(
                "Vault created successfully."
            )

            st.info(
                "Please refresh the app."
            )

# =====================================================
# UNLOCK VAULT
# =====================================================

def unlock_vault():

    st.title("🔓 Unlock Vault")

    password = st.text_input(

        "Enter Master Password",

        type="password"
    )

    if st.button("Unlock Vault"):

        if not os.path.exists(
            MASTER_FILE
        ):

            st.error(
                "Master password not found."
            )

            return

        with open(
            MASTER_FILE,
            "r"
        ) as f:

            stored_hash = f.read().strip()

        entered_hash = hash_password(
            password
        )

        if entered_hash == stored_hash:

            st.session_state[
                "vault_unlocked"
            ] = True

            st.rerun()

        else:

            st.error(
                "Incorrect password."
            )

# =====================================================
# CHANGE MASTER PASSWORD
# =====================================================

def change_master_password(

    current_password,
    new_password
):

    try:

        if not os.path.exists(
            MASTER_FILE
        ):

            return (
                False,
                "Master password file missing."
            )

        with open(
            MASTER_FILE,
            "r"
        ) as f:

            stored_hash = f.read().strip()

        current_hash = hash_password(
            current_password
        )

        if current_hash != stored_hash:

            return (
                False,
                "Current password is incorrect."
            )

        new_hash = hash_password(
            new_password
        )

        with open(
            MASTER_FILE,
            "w"
        ) as f:

            f.write(new_hash)

        return (
            True,
            "Password updated successfully."
        )

    except Exception as e:

        return (
            False,
            str(e)
        )