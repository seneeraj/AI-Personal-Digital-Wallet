import streamlit as st

from sqlalchemy import select

from database.models import documents
from database.db_manager import engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Search",
    page_icon="🔍",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🔍 Smart Document Search")

st.caption(
    "Search documents using names, "
    "tags, notes, OCR text, or categories."
)

st.divider()

# =====================================================
# SEARCH INPUT
# =====================================================

search_query = st.text_input(

    "🔎 Search your vault",

    placeholder=(
        "Example: PAN card, "
        "medical report, passport"
    )
)

# =====================================================
# CATEGORY FILTER
# =====================================================

categories = [

    "All",

    "Personal",
    "Financial",
    "Medical",
    "Education",
    "Legal",
    "Uncategorized"
]

selected_category = st.selectbox(

    "📂 Filter by Category",

    categories
)

st.divider()

# =====================================================
# LOAD DOCUMENTS
# =====================================================

query = select(documents)

with engine.connect() as conn:

    results = conn.execute(query).fetchall()

# =====================================================
# SEARCH RESULTS
# =====================================================

filtered_results = []

for row in results:

    searchable_text = (

        str(row.document_name)
        + " "
        + str(row.document_category)
        + " "
        + str(row.tags)
        + " "
        + str(row.notes)
        + " "
        + str(row.ocr_text)

    ).lower()

    # =============================================
    # SEARCH MATCH
    # =============================================

    query_match = (
        search_query.lower()
        in searchable_text
    )

    # =============================================
    # CATEGORY MATCH
    # =============================================

    if selected_category == "All":

        category_match = True

    else:

        category_match = (

            row.document_category
            == selected_category
        )

    # =============================================
    # FINAL FILTER
    # =============================================

    if query_match and category_match:

        filtered_results.append(row)

# =====================================================
# RESULT COUNT
# =====================================================

st.subheader(
    f"📄 Results Found: "
    f"{len(filtered_results)}"
)

# =====================================================
# EMPTY STATE
# =====================================================

if not filtered_results:

    st.info(
        "No matching documents found."
    )

# =====================================================
# DISPLAY RESULTS
# =====================================================

else:

    cols = st.columns(2)

    for index, row in enumerate(filtered_results):

        with cols[index % 2]:

            st.markdown(
                """
                <div style="
                    border:1px solid #2d3748;
                    border-radius:15px;
                    padding:20px;
                    margin-bottom:20px;
                    background:#111827;
                ">
                """,
                unsafe_allow_html=True
            )

            # =====================================
            # DOCUMENT NAME
            # =====================================

            st.subheader(
                f"📄 {row.document_name}"
            )

            # =====================================
            # CATEGORY
            # =====================================

            st.caption(
                f"📂 {row.document_category}"
            )

            # =====================================
            # TAGS
            # =====================================

            if row.tags:

                st.write(
                    f"🏷️ {row.tags}"
                )

            # =====================================
            # NOTES
            # =====================================

            if row.notes:

                st.write(
                    f"📝 {row.notes}"
                )

            # =====================================
            # OCR PREVIEW
            # =====================================

            if row.ocr_text:

                preview = (
                    row.ocr_text[:250]
                    + "..."
                )

                st.caption(
                    f"📖 OCR Preview: {preview}"
                )

            # =====================================
            # UPLOAD DATE
            # =====================================

            st.caption(
                f"📅 Uploaded: "
                f"{row.upload_date}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )