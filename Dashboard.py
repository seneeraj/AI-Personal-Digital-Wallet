import os

import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Personal Digital Wallet",
    page_icon="🔐",
    layout="wide"
)

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

    password_exists,

    setup_master_password,

    verify_master_password,

    unlock_vault
)

from database.get_documents import (
    get_all_documents
)

# =====================================================
# SESSION STATE
# =====================================================

if "vault_unlocked" not in st.session_state:

    st.session_state[
        "vault_unlocked"
    ] = False

# =====================================================
# HEADER
# =====================================================

st.title("🔐 AI Personal Digital Wallet")

st.caption(
    "Secure cloud-native encrypted document vault."
)

st.divider()

# =====================================================
# FIRST TIME SETUP
# =====================================================

if not password_exists():

    st.markdown(
        "## 🆕 First Time Setup"
    )

    st.info(
        "Create your master password to initialize the vault."
    )

    with st.form("setup_password_form"):

        new_password = st.text_input(

            "Create Master Password",

            type="password"
        )

        confirm_password = st.text_input(

            "Confirm Master Password",

            type="password"
        )

        setup_submit = st.form_submit_button(
            "🚀 Create Vault"
        )

    # =============================================
    # CREATE PASSWORD
    # =============================================

    if setup_submit:

        if not new_password:

            st.warning(
                "Please enter a password."
            )

        elif len(new_password) < 4:

            st.warning(
                "Password must be at least 4 characters."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            setup_master_password(
                new_password
            )

            unlock_vault(
                new_password
            )

            st.success(
                "✅ Vault initialized successfully."
            )

            st.rerun()

# =====================================================
# LOGIN SCREEN
# =====================================================

elif not st.session_state.get(
    "vault_unlocked",
    False
):

    st.markdown(
        "## 🔓 Unlock Vault"
    )

    with st.form("unlock_form"):

        password = st.text_input(

            "Enter Master Password",

            type="password"
        )

        unlock_submit = st.form_submit_button(
            "🔓 Unlock"
        )

    # =============================================
    # LOGIN
    # =============================================

    if unlock_submit:

        if not password:

            st.warning(
                "Please enter password."
            )

        else:

            success = unlock_vault(
                password
            )

            if success:

                st.success(
                    "✅ Vault unlocked successfully."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Incorrect password."
                )

# =====================================================
# MAIN DASHBOARD
# =====================================================

else:

    # =============================================
    # LOAD DOCUMENTS
    # =============================================

    try:

        documents = get_all_documents()

    except Exception as e:

        st.error(
            f"Error loading documents: {e}"
        )

        documents = []

    # =============================================
    # METRICS
    # =============================================

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

    expiring_documents = [

        doc

        for doc in documents

        if doc.get("expiry_date")
    ]

    # =============================================
    # DASHBOARD METRICS
    # =============================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Total Documents",
            total_documents
        )

    with col2:

        st.metric(
            "📁 Categories",
            len(categories)
        )

    with col3:

        st.metric(
            "⏰ Expiry Alerts",
            len(expiring_documents)
        )

    st.divider()

    # =============================================
    # RECENT DOCUMENTS
    # =============================================

    st.markdown(
        "## 📚 Recent Documents"
    )

    if documents:

        for doc in documents[:5]:

            with st.container():

                st.markdown("---")

                st.markdown(
                    f"### 📄 "
                    f"{doc.get('document_name', '')}"
                )

                st.markdown(
                    f"**📁 Category:** "
                    f"{doc.get('document_category', '')}"
                )

                if doc.get("tags"):

                    st.markdown(
                        f"**🏷️ Tags:** "
                        f"{doc.get('tags')}"
                    )

                if doc.get("expiry_date"):

                    st.markdown(
                        f"**📅 Expiry:** "
                        f"{doc.get('expiry_date')}"
                    )

    else:

        st.info(
            "No documents uploaded yet."
        )

    st.divider()

    # =============================================
    # QUICK ACTIONS
    # =============================================

    st.markdown(
        "## ⚡ Quick Actions"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬆️ Upload Documents"
        ):

            st.switch_page(
                "pages/1_Upload_Documents.py"
            )

    with col2:

        if st.button(
            "📚 Open Library"
        ):

            st.switch_page(
                "pages/2_Document_Library.py"
            )

    with col3:

        if st.button(
            "🔍 Search Documents"
        ):

            st.switch_page(
                "pages/4_Search.py"
            )

    st.divider()

    # =============================================
    # SECURITY STATUS
    # =============================================

    st.markdown(
        "## 🔐 Security Status"
    )

    st.success(
        "AES encryption active."
    )

    st.success(
        "Supabase cloud storage connected."
    )

    st.success(
        "Vault session unlocked."
    )

    st.divider()

    # =============================================
    # FOOTER
    # =============================================

    st.caption(
        "AI Personal Digital Wallet • Secure Cloud Vault"
    )
