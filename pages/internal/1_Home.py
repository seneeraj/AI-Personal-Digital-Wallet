import streamlit as st
import pandas as pd

from sqlalchemy import select

from database.models import documents
from database.db_manager import engine

from modules.ai.reminder_engine import (
    calculate_expiry_alert
)

# =====================================================
# VAULT PROTECTION
# =====================================================

if "vault_unlocked" not in st.session_state:
    st.warning("Vault locked")
    st.stop()

if not st.session_state["vault_unlocked"]:
    st.warning("Please unlock vault")
    st.stop()

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏠 AI Digital Vault Dashboard")

st.write(
    "Welcome to your AI-powered secure document vault."
)

# =====================================================
# FETCH DOCUMENTS
# =====================================================

query = select(documents)

with engine.connect() as conn:

    results = conn.execute(query).fetchall()

# =====================================================
# DOCUMENT STATISTICS
# =====================================================

total_documents = len(results)

personal_count = 0
financial_count = 0
medical_count = 0
education_count = 0
legal_count = 0
uncategorized_count = 0

for row in results:

    category = row.document_category

    if category == "Personal":
        personal_count += 1

    elif category == "Financial":
        financial_count += 1

    elif category == "Medical":
        medical_count += 1

    elif category == "Education":
        education_count += 1

    elif category == "Legal":
        legal_count += 1

    else:
        uncategorized_count += 1

# =====================================================
# TOP METRICS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📄 Total Documents",
        total_documents
    )

with col2:
    st.metric(
        "🏥 Medical Records",
        medical_count
    )

with col3:
    st.metric(
        "💰 Financial Docs",
        financial_count
    )

# =====================================================
# CATEGORY DISTRIBUTION
# =====================================================

st.subheader("📊 AI Document Categories")

category_data = pd.DataFrame({

    "Category": [

        "Personal",
        "Financial",
        "Medical",
        "Education",
        "Legal",
        "Uncategorized"
    ],

    "Count": [

        personal_count,
        financial_count,
        medical_count,
        education_count,
        legal_count,
        uncategorized_count
    ]
})

st.bar_chart(
    category_data.set_index("Category")
)

# =====================================================
# RECENT DOCUMENTS
# =====================================================

st.subheader("🕒 Recent Uploads")

recent_docs = []

for row in results[-5:]:

    recent_docs.append({

        "Document": row.document_name,

        "Category": row.document_category,

        "Upload Date": row.upload_date
    })

if recent_docs:

    recent_df = pd.DataFrame(recent_docs)

    st.dataframe(
        recent_df,
        use_container_width=True
    )

else:

    st.info("No documents uploaded yet.")

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🤖 AI Vault Insights")

if medical_count > 5:

    st.warning(
        "You have many medical documents stored. "
        "Consider creating a dedicated health timeline."
    )

if financial_count > 5:

    st.info(
        "Your vault contains multiple financial records."
    )

if uncategorized_count > 0:

    st.warning(
        f"{uncategorized_count} documents "
        "could not be categorized automatically."
    )

if total_documents == 0:

    st.info(
        "Upload your first document to start "
        "building your AI vault."
    )
    
# =====================================================
# SMART REMINDERS & ALERTS
# =====================================================

st.subheader("🔔 Smart Alerts & Reminders")

alert_found = False

for row in results:

    if row.expiry_date:

        alert_message = calculate_expiry_alert(
            row.expiry_date
        )

        if alert_message:

            alert_found = True

            st.warning(

                f"{row.document_name} | "
                f"{row.expiry_date} | "
                f"{alert_message}"
            )

if not alert_found:

    st.info(
        "No active reminders or expiry alerts."
    )