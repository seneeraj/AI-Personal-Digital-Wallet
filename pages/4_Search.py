import os

import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Search Documents",

    page_icon="🔍",

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

from database.get_documents import (
    get_all_documents
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🔍 Search Documents")

st.caption(
    "Search documents using names, tags, OCR text and categories."
)

st.divider()

# =====================================================
# FETCH DOCUMENTS
# =====================================================

try:

    documents = get_all_documents()

except Exception as e:

    st.error(
        f"Error loading documents: {e}"
    )

    st.stop()

# =====================================================
# EMPTY STATE
# =====================================================

if not documents:

    st.info(
        "No documents found."
    )

    st.stop()

# =====================================================
# SEARCH INPUT
# =====================================================

search_query = st.text_input(

    "🔍 Search",

    placeholder=(
        "Search by document name, "
        "OCR text, tags, category..."
    )
)

# =====================================================
# CATEGORY FILTER
# =====================================================

categories = list(

    set(

        doc.get(
            "document_category",
            "Other"
        )

        for doc in documents
    )
)

categories.sort()

selected_category = st.selectbox(

    "📁 Filter Category",

    ["All"] + categories
)

st.divider()

# =====================================================
# SEARCH RESULTS
# =====================================================

results = []

for doc in documents:

    document_name = str(

        doc.get(
            "document_name",
            ""
        )
    )

    document_category = str(

        doc.get(
            "document_category",
            ""
        )
    )

    tags = str(

        doc.get(
            "tags",
            ""
        )
    )

    ocr_text = str(

        doc.get(
            "ocr_text",
            ""
        )
    )

    combined_text = (

        document_name
        + " "
        + document_category
        + " "
        + tags
        + " "
        + ocr_text
    ).lower()

    matches_search = (

        search_query.lower()
        in combined_text
    )

    matches_category = (

        selected_category == "All"

        or

        document_category == selected_category
    )

    if matches_search and matches_category:

        results.append(doc)

# =====================================================
# RESULT COUNT
# =====================================================

st.markdown(

    f"### 📄 Search Results: "
    f"{len(results)}"
)

st.divider()

# =====================================================
# DISPLAY RESULTS
# =====================================================

if results:

    for row in results:

        with st.container():

            st.markdown("---")

            st.markdown(
                f"## 📄 "
                f"{row.get('document_name', '')}"
            )

            st.markdown(
                f"**📁 Category:** "
                f"{row.get('document_category', '')}"
            )

            if row.get("tags"):

                st.markdown(
                    f"**🏷️ Tags:** "
                    f"{row.get('tags')}"
                )

            if row.get("expiry_date"):

                st.markdown(
                    f"**📅 Expiry Date:** "
                    f"{row.get('expiry_date')}"
                )

            if row.get("notes"):

                st.markdown(
                    f"**📝 Notes:** "
                    f"{row.get('notes')}"
                )

            upload_date = row.get(
                "upload_date"
            )

            if upload_date:

                st.markdown(
                    f"**⏱️ Uploaded:** "
                    f"{upload_date}"
                )

else:

    st.warning(
        "No matching documents found."
    )

# =====================================================
# SUMMARY TABLE
# =====================================================

st.divider()

summary_data = []

for row in results:

    summary_data.append({

        "Document":
            row.get("document_name"),

        "Category":
            row.get("document_category"),

        "Expiry":
            row.get("expiry_date"),

        "Tags":
            row.get("tags")
    })

summary_df = pd.DataFrame(
    summary_data
)

st.dataframe(

    summary_df,

    use_container_width=True
)
