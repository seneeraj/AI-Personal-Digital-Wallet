import os

import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Edit Document",

    page_icon="✏️",

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
# IMPORT MODULES
# =====================================================

from database.supabase_client import (
    supabase
)

# =====================================================
# VALIDATE SESSION
# =====================================================

if "edit_document_id" not in st.session_state:

    st.warning(
        "No document selected."
    )

    st.stop()

document_id = st.session_state[
    "edit_document_id"
]

# =====================================================
# FETCH DOCUMENT
# =====================================================

response = (

    supabase
    .table("documents")
    .select("*")
    .eq("id", document_id)
    .execute()
)

if not response.data:

    st.error(
        "Document not found."
    )

    st.stop()

document = response.data[0]

# =====================================================
# PAGE TITLE
# =====================================================

st.title("✏️ Edit Document")

st.divider()

# =====================================================
# FORM
# =====================================================

with st.form("edit_document_form"):

    document_name = st.text_input(

        "📄 Document Name",

        value=document.get(
            "document_name",
            ""
        )
    )

    document_category = st.selectbox(

        "📁 Category",

        [
            "Personal",
            "Financial",
            "Medical",
            "Educational",
            "Legal",
            "Other"
        ],

        index=0
    )

    tags = st.text_input(

        "🏷️ Tags",

        value=document.get(
            "tags",
            ""
        )
    )

    notes = st.text_area(

        "📝 Notes",

        value=document.get(
            "notes",
            ""
        )
    )

    expiry_date = st.text_input(

        "📅 Expiry Date",

        value=str(

            document.get(
                "expiry_date",
                ""
            )
        )
    )

    submitted = st.form_submit_button(
        "💾 Save Changes"
    )

# =====================================================
# UPDATE DOCUMENT
# =====================================================

if submitted:

    try:

        (

            supabase
            .table("documents")
            .update({

                "document_name":
                    document_name,

                "document_category":
                    document_category,

                "tags":
                    tags,

                "notes":
                    notes,

                "expiry_date":
                    expiry_date
            })

            .eq(
                "id",
                document_id
            )

            .execute()
        )

        st.success(
            "Document updated successfully."
        )

    except Exception as e:

        st.error(
            f"Update failed: {e}"
        )