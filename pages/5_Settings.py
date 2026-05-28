import os

import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Settings",

    page_icon="⚙️",

    layout="wide"
)

# =====================================================
# AUTH GUARD
# =====================================================

from security.auth_guard import (
    require_login
)

require_login()

# =====================================================
# LOAD CSS
# =====================================================

def load_css():

    css_path = "assets/style.css"

    if os.path.exists(css_path):

        with open(

            css_path,

            "r",

            encoding="utf-8"

        ) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True
            )

load_css()

# =====================================================
# IMPORTS
# =====================================================

from security.master_auth import (

    verify_master_password,

    change_master_password
)

from database.get_documents import (
    get_all_documents
)

from database.supabase_client import (
    supabase
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("⚙️ Settings")

st.caption(
    "Manage security, storage and application preferences."
)

st.divider()

# =====================================================
# SECURITY SETTINGS
# =====================================================

st.markdown("## 🔐 Security Settings")

with st.form("change_password_form"):

    current_password = st.text_input(

        "Current Master Password",

        type="password"
    )

    new_password = st.text_input(

        "New Master Password",

        type="password"
    )

    confirm_password = st.text_input(

        "Confirm New Password",

        type="password"
    )

    password_submit = st.form_submit_button(
        "🔄 Change Password"
    )

# =====================================================
# CHANGE PASSWORD
# =====================================================

if password_submit:

    try:

        # =============================================
        # VALIDATIONS
        # =============================================

        if not current_password:

            st.warning(
                "Enter current password."
            )

        elif not new_password:

            st.warning(
                "Enter new password."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            # =========================================
            # VERIFY CURRENT PASSWORD
            # =========================================

            valid = verify_master_password(
                current_password
            )

            if not valid:

                st.error(
                    "Current password is incorrect."
                )

            else:

                # =====================================
                # UPDATE PASSWORD
                # =====================================

                change_master_password(
                    new_password
                )

                st.success(
                    "✅ Master password updated successfully."
                )

    except Exception as e:

        st.error(
            f"Password update failed: {e}"
        )

st.divider()

# =====================================================
# STORAGE SUMMARY
# =====================================================

st.markdown("## ☁️ Storage Summary")

try:

    documents = get_all_documents()

    total_documents = len(documents)

    categories = list(

        set(

            doc.get(
                "document_category",
                "Other"
            )

            for doc in documents
        )
    )

    st.metric(
        "📄 Total Documents",
        total_documents
    )

    st.metric(
        "📁 Categories",
        len(categories)
    )

except Exception as e:

    st.error(
        f"Error loading summary: {e}"
    )

st.divider()

# =====================================================
# SUPABASE CONNECTION STATUS
# =====================================================

st.markdown("## 🔌 Cloud Connection")

try:

    test_response = (

        supabase
        .table("documents")
        .select("id")
        .limit(1)
        .execute()
    )

    st.success(
        "✅ Connected to Supabase successfully."
    )

except Exception as e:

    st.error(
        f"Supabase connection failed: {e}"
    )

st.divider()

# =====================================================
# SESSION SETTINGS
# =====================================================

st.markdown("## 🧠 Session Information")

vault_status = st.session_state.get(

    "vault_unlocked",

    False
)

st.write(
    f"🔓 Vault Status: "
    f"{'Unlocked' if vault_status else 'Locked'}"
)

if st.button("🔒 Lock Vault"):

    st.session_state[
        "vault_unlocked"
    ] = False

    st.success(
        "Vault locked successfully."
    )

    st.switch_page(
        "Dashboard.py"
    )

st.divider()

# =====================================================
# APP INFORMATION
# =====================================================

st.markdown("## ℹ️ Application Information")

st.info(
    """
AI Personal Digital Wallet

Features:
- AES encrypted storage
- Supabase cloud persistence
- OCR document extraction
- AI-based tagging
- Expiry tracking
- Secure document management
"""
)

# =====================================================
# DANGER ZONE
# =====================================================

st.markdown("## ⚠️ Danger Zone")

with st.expander("Delete All Documents"):

    st.warning(
        "This action cannot be undone."
    )

    confirm_delete = st.checkbox(
        "I understand the risks."
    )

    if st.button(
        "🗑️ Delete Everything"
    ):

        if confirm_delete:

            try:

                # =====================================
                # FETCH DOCUMENTS
                # =====================================

                documents = get_all_documents()

                # =====================================
                # DELETE STORAGE FILES
                # =====================================

                for doc in documents:

                    encrypted_path = doc.get(
                        "encrypted_path"
                    )

                    if encrypted_path:

                        try:

                            (
                                supabase.storage
                                .from_(
                                    "encrypted-documents"
                                )
                                .remove(
                                    [encrypted_path]
                                )
                            )

                        except Exception:

                            pass

                # =====================================
                # DELETE DATABASE RECORDS
                # =====================================

                (
                    supabase
                    .table("documents")
                    .delete()
                    .neq("id", 0)
                    .execute()
                )

                st.success(
                    "All documents deleted successfully."
                )

            except Exception as e:

                st.error(
                    f"Delete failed: {e}"
                )
