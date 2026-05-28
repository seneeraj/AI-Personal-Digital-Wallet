import streamlit as st

from sqlalchemy import select

from database.models import documents
from database.db_manager import engine

from database.update_metadata import (
    update_document_metadata
)

from database.update_category import (
    update_document_category
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Edit Document",
    page_icon="✏️",
    layout="centered"
)

# =====================================================
# TITLE
# =====================================================

st.title("✏️ Edit Document")

# =====================================================
# GET DOCUMENT ID
# =====================================================

selected_document_id = st.session_state.get(
    "selected_document_id"
)

# =====================================================
# NO DOCUMENT SELECTED
# =====================================================

if not selected_document_id:

    st.warning(
        "No document selected."
    )

    if st.button("⬅ Back to Library"):

        st.switch_page(
            "pages/2_Document_Library.py"
        )

    st.stop()

# =====================================================
# LOAD DOCUMENT
# =====================================================

query = select(documents).where(
    documents.c.id == selected_document_id
)

with engine.connect() as conn:

    row = conn.execute(query).fetchone()

# =====================================================
# DOCUMENT NOT FOUND
# =====================================================

if not row:

    st.error(
        "Document not found."
    )

    if st.button("⬅ Back to Library"):

        st.switch_page(
            "pages/2_Document_Library.py"
        )

    st.stop()

# =====================================================
# DOCUMENT DETAILS
# =====================================================

st.subheader(
    f"📄 {row.document_name}"
)

st.caption(
    f"📅 Uploaded: {row.upload_date}"
)

st.divider()

# =====================================================
# CATEGORY
# =====================================================

categories = [

    "Personal",
    "Financial",
    "Medical",
    "Education",
    "Legal",
    "Uncategorized"
]

current_category = (

    row.document_category

    if row.document_category in categories

    else "Uncategorized"
)

new_category = st.selectbox(

    "📂 Category",

    categories,

    index=categories.index(
        current_category
    )
)

# =====================================================
# TAGS
# =====================================================

new_tags = st.text_input(

    "🏷️ Tags",

    value=row.tags if row.tags else ""
)

# =====================================================
# NOTES
# =====================================================

new_notes = st.text_area(

    "📝 Notes",

    value=row.notes if row.notes else "",

    height=150
)

# =====================================================
# EXPIRY DATE
# =====================================================

expiry_value = (
    row.expiry_date
    if row.expiry_date
    else "Not detected"
)

st.info(
    f"📅 Expiry Date: {expiry_value}"
)

st.divider()

# =====================================================
# BUTTONS
# =====================================================

col1, col2 = st.columns(2)

# =====================================================
# SAVE
# =====================================================

with col1:

    if st.button("💾 Save Changes"):

        update_document_category(

            document_id=row.id,

            new_category=new_category
        )

        update_document_metadata(

            document_id=row.id,

            tags=new_tags,

            notes=new_notes
        )

        st.success(
            "✅ Document updated successfully."
        )

# =====================================================
# BACK
# =====================================================

with col2:

    if st.button("⬅ Back to Library"):

        st.switch_page(
            "pages/2_Document_Library.py"
        )