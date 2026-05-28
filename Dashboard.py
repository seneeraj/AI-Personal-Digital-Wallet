import streamlit as st
import os

from datetime import datetime, timedelta

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Digital Vault",
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
# CREATE REQUIRED FOLDERS
# =====================================================

os.makedirs(
    "encrypted_storage",
    exist_ok=True
)

os.makedirs(
    "uploads/temp",
    exist_ok=True
)

os.makedirs(
    "temp_decrypted",
    exist_ok=True
)

os.makedirs(
    "security",
    exist_ok=True
)

# =====================================================
# IMPORT AUTH
# =====================================================

from security.master_auth import (
    setup_master_password,
    unlock_vault
)

# =====================================================
# IMPORT DATABASE
# =====================================================

from database.init_db import (
    initialize_database
)

from sqlalchemy import select

from database.models import documents
from database.db_manager import engine

# =====================================================
# INITIALIZE DATABASE
# =====================================================

initialize_database()

# =====================================================
# SESSION CONFIG
# =====================================================

SESSION_TIMEOUT_MINUTES = 5

# =====================================================
# SESSION STATE
# =====================================================

if "vault_unlocked" not in st.session_state:

    st.session_state["vault_unlocked"] = False

if "last_activity" not in st.session_state:

    st.session_state["last_activity"] = None

# =====================================================
# AUTO SESSION EXPIRY
# =====================================================

if (

    st.session_state["vault_unlocked"]

    and

    st.session_state["last_activity"]

):

    elapsed = (

        datetime.now()

        -

        st.session_state["last_activity"]
    )

    if elapsed > timedelta(

        minutes=SESSION_TIMEOUT_MINUTES
    ):

        st.session_state[
            "vault_unlocked"
        ] = False

        st.warning(
            "🔒 Session expired. Please login again."
        )

        st.rerun()

# =====================================================
# AUTHENTICATION
# =====================================================

MASTER_FILE = "security/master.hash"

needs_setup = False

# =====================================================
# CHECK MASTER PASSWORD FILE
# =====================================================

if not os.path.exists(MASTER_FILE):

    needs_setup = True

else:

    try:

        with open(
            MASTER_FILE,
            "r"
        ) as f:

            stored_hash = f.read().strip()

        if not stored_hash:

            needs_setup = True

    except:

        needs_setup = True

# =====================================================
# FIRST TIME SETUP
# =====================================================

if needs_setup:

    setup_master_password()

    st.stop()

# =====================================================
# LOCKED STATE
# =====================================================

if not st.session_state["vault_unlocked"]:

    unlock_vault()

    st.stop()

# =====================================================
# UPDATE LAST ACTIVITY
# =====================================================

st.session_state[
    "last_activity"
] = datetime.now()

# =====================================================
# LOAD DOCUMENTS
# =====================================================

query = select(documents)

with engine.connect() as conn:

    results = conn.execute(query).fetchall()

# =====================================================
# DASHBOARD
# =====================================================

st.title("🏠 Dashboard")

st.caption(
    "Welcome to your AI-powered "
    "secure digital vault."
)

st.divider()

# =====================================================
# TOP METRICS
# =====================================================

total_documents = len(results)

categories = set()

documents_with_expiry = 0

for row in results:

    if row.document_category:

        categories.add(
            row.document_category
        )

    if row.expiry_date:

        documents_with_expiry += 1

col1, col2, col3 = st.columns(3)

# =====================================================
# TOTAL DOCUMENTS
# =====================================================

with col1:

    st.metric(
        "📄 Total Documents",
        total_documents
    )

# =====================================================
# CATEGORIES
# =====================================================

with col2:

    st.metric(
        "📂 Categories",
        len(categories)
    )

# =====================================================
# EXPIRY TRACKING
# =====================================================

with col3:

    st.metric(
        "📅 Expiry Tracking",
        documents_with_expiry
    )

st.divider()

# =====================================================
# QUICK ACTIONS
# =====================================================

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

# =====================================================
# UPLOAD
# =====================================================

with col1:

    if st.button("⬆ Upload Documents"):

        st.switch_page(
            "pages/1_Upload_Documents.py"
        )

# =====================================================
# LIBRARY
# =====================================================

with col2:

    if st.button("📚 Open Document Library"):

        st.switch_page(
            "pages/2_Document_Library.py"
        )

# =====================================================
# SEARCH
# =====================================================

with col3:

    if st.button("🔍 Smart Search"):

        st.switch_page(
            "pages/4_Search.py"
        )

st.divider()

# =====================================================
# RECENT DOCUMENTS
# =====================================================

st.subheader("🕒 Recent Uploads")

recent_docs = results[-5:]

if not recent_docs:

    st.info(
        "No documents uploaded yet."
    )

else:

    recent_data = []

    for row in reversed(recent_docs):

        recent_data.append({

            "Document": row.document_name,

            "Category": row.document_category,

            "Upload Date": row.upload_date
        })

    st.dataframe(
        recent_data,
        use_container_width=True
    )

st.divider()

# =====================================================
# SMART ALERTS
# =====================================================

st.subheader("🔔 Smart Alerts & Reminders")

expiry_docs = []

today = datetime.now()

for row in results:

    if row.expiry_date:

        try:

            parsed_expiry = None

            expiry_str = str(
                row.expiry_date
            )

            date_formats = [

                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y"
            ]

            for fmt in date_formats:

                try:

                    parsed_expiry = datetime.strptime(
                        expiry_str,
                        fmt
                    )

                    break

                except:
                    pass

            if parsed_expiry:

                days_left = (
                    parsed_expiry - today
                ).days

                expiry_docs.append(
                    (
                        row,
                        days_left
                    )
                )

        except:
            pass

# =====================================================
# DISPLAY ALERTS
# =====================================================

if not expiry_docs:

    st.success(
        "No expiry alerts detected."
    )

else:

    for row, days_left in expiry_docs:

        # =============================================
        # EXPIRED
        # =============================================

        if days_left < 0:

            st.error(
                f"""
                ❌ {row.document_name}

                Expired on:
                {row.expiry_date}
                """
            )

        # =============================================
        # EXPIRING SOON
        # =============================================

        elif days_left <= 30:

            st.warning(
                f"""
                ⚠ {row.document_name}

                Expires in {days_left} days

                Expiry Date:
                {row.expiry_date}
                """
            )

        # =============================================
        # VALID
        # =============================================

        else:

            st.success(
                f"""
                ✅ {row.document_name}

                | {row.expiry_date}

                | Valid for {days_left} more days
                """
            )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🔐 AI Digital Vault")

    st.success("Vault Unlocked")

    st.divider()

    st.markdown(
        f"""
        ### 📌 Available Modules

        - ⬆ Upload Documents
        - 📚 Document Library
        - 🔍 Smart Search
        - ⚙️ Settings

        ---
        
        ⏱️ Auto-lock after:
        {SESSION_TIMEOUT_MINUTES} minutes
        """
    )

    st.divider()

    # =================================================
    # LOCK BUTTON
    # =================================================

    if st.button("🔒 Lock Vault"):

        st.session_state[
            "vault_unlocked"
        ] = False

        st.session_state[
            "last_activity"
        ] = None

        st.rerun()

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🚀 AI Digital Vault "
    "| Intelligent Secure "
    "Document Management"
)