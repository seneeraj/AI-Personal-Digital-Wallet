import os
import hashlib
import streamlit as st

# =====================================================
# PASSWORD FILE
# =====================================================

PASSWORD_FILE = "master_password.hash"

# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()

# =====================================================
# PASSWORD EXISTS
# =====================================================

def password_exists():

    return os.path.exists(
        PASSWORD_FILE
    )

# =====================================================
# SAVE MASTER PASSWORD
# =====================================================

def save_master_password(password):

    hashed_password = hash_password(
        password
    )

    with open(

        PASSWORD_FILE,

        "w"

    ) as f:

        f.write(hashed_password)

# =====================================================
# SETUP MASTER PASSWORD
# =====================================================

def setup_master_password(password):

    save_master_password(
        password
    )

# =====================================================
# VERIFY MASTER PASSWORD
# =====================================================

def verify_master_password(password):

    if not password_exists():

        return False

    with open(

        PASSWORD_FILE,

        "r"

    ) as f:

        saved_hash = f.read()

    return (

        hash_password(password)

        ==

        saved_hash
    )

# =====================================================
# CHANGE MASTER PASSWORD
# =====================================================

def change_master_password(new_password):

    save_master_password(
        new_password
    )

# =====================================================
# UNLOCK VAULT
# =====================================================

def unlock_vault(password):

    valid = verify_master_password(
        password
    )

    if valid:

        st.session_state[
            "vault_unlocked"
        ] = True

        return True

    return False

# =====================================================
# LOCK VAULT
# =====================================================

def lock_vault():

    st.session_state[
        "vault_unlocked"
    ] = False
