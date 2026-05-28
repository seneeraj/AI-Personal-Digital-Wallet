import os
import tempfile
import traceback
from datetime import datetime

import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Document Library",
    page_icon="📚",
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

from database.get_documents import (
    get_all_documents
)

from database.supabase_client import (
    supabase
)

from modules.encryption.aes_decryptor import (
    decrypt_file
)

# =====================================================
# CREATE TEMP DIRECTORY
# =====================================================

os.makedirs(
    "temp_decrypted",
    exist_ok=True
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("📚 Document Library")

st.caption(
    "Browse, search and manage your encrypted documents."
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
# SEARCH + FILTERS
# =====================================================

col1, col2 = st.columns([2, 1])

with col1:

    search_query = st.text_input(

        "🔍 Search Documents",

        placeholder="Search by name, tags, category..."
    )

with col2:

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

# =====================================================
# FILTER DOCUMENTS
# =====================================================

filtered_documents = []

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

    # =============================================
    # SEARCH FILTER
    # =============================================

    matches_search = (

        search_query.lower()
        in (
            document_name
            + " "
            + document_category
            + " "
            + tags
        ).lower()
    )

    # =============================================
    # CATEGORY FILTER
    # =============================================

    matches_category = (

        selected_category == "All"

        or

        document_category == selected_category
    )

    if matches_search and matches_category:

        filtered_documents.append(doc)

# =====================================================
# DOCUMENT COUNT
# =====================================================

st.markdown(

    f"### 📄 Total Documents: "
    f"{len(filtered_documents)}"
)

st.divider()

# =====================================================
# DISPLAY DOCUMENTS
# =====================================================

for row in filtered_documents:

    try:

        document_name = row.get(
            "document_name",
            "Unknown"
        )

        document_category = row.get(
            "document_category",
            "Other"
        )

        expiry_date = row.get(
            "expiry_date"
        )

        tags = row.get(
            "tags",
            ""
        )

        notes = row.get(
            "notes",
            ""
        )

        upload_date = row.get(
            "upload_date"
        )

        encrypted_path = row.get(
            "encrypted_path"
        )

        # =========================================
        # CARD
        # =========================================

        with st.container():

            st.markdown("---")

            col1, col2 = st.columns([4, 1])

            # =====================================
            # LEFT SIDE
            # =====================================

            with col1:

                st.markdown(
                    f"## 📄 {document_name}"
                )

                st.markdown(
                    f"**📁 Category:** "
                    f"{document_category}"
                )

                if tags:

                    st.markdown(
                        f"**🏷️ Tags:** "
                        f"{tags}"
                    )

                if notes:

                    st.markdown(
                        f"**📝 Notes:** "
                        f"{notes}"
                    )

                if expiry_date:

                    st.markdown(
                        f"**📅 Expiry:** "
                        f"{expiry_date}"
                    )

                if upload_date:

                    st.markdown(
                        f"**⏱️ Uploaded:** "
                        f"{upload_date}"
                    )

            # =====================================
            # RIGHT SIDE
            # =====================================

            with col2:

                # =================================
                # DOWNLOAD ENCRYPTED FILE
                # =================================

                if st.button(

                    "👁️ View",

                    key=f"view_{row['id']}"
                ):

                    try:

                        # =========================
                        # DOWNLOAD FROM SUPABASE
                        # =========================

                        file_bytes = (

                            supabase.storage
                            .from_(
                                "encrypted-documents"
                            )
                            .download(
                                encrypted_path
                            )
                        )

                        # =========================
                        # SAVE TEMP ENCRYPTED FILE
                        # =========================

                        temp_encrypted_path = os.path.join(

                            "temp_decrypted",

                            encrypted_path
                        )

                        with open(
                            temp_encrypted_path,
                            "wb"
                        ) as f:

                            f.write(file_bytes)

                        # =========================
                        # DECRYPT TEMP FILE
                        # =========================

                        decrypted_output_path = os.path.join(

                            "temp_decrypted",

                            document_name
                        )

                        decrypt_file(

                            temp_encrypted_path,

                            decrypted_output_path
                        )

                        # =========================
                        # OPEN FILE
                        # =========================

                        with open(

                            decrypted_output_path,

                            "rb"
                        ) as file:

                            st.download_button(

                                label="⬇️ Download",

                                data=file,

                                file_name=document_name,

                                mime="application/octet-stream",

                                key=f"download_{row['id']}"
                            )

                        st.success(
                            "Document ready."
                        )

                    except Exception as e:

                        st.error(
                            f"View failed: {e}"
                        )

                        st.code(
                            traceback.format_exc()
                        )

                # =================================
                # EDIT BUTTON
                # =================================

                if st.button(

                    "✏️ Edit",

                    key=f"edit_{row['id']}"
                ):

                    st.session_state[
                        "edit_document_id"
                    ] = row["id"]

                    st.switch_page(
                        "pages/3_edit_document.py"
                    )

    except Exception as e:

        st.error(
            f"Error displaying document: {e}"
        )

        st.code(
            traceback.format_exc()
        )

# =====================================================
# SUMMARY TABLE
# =====================================================

st.divider()

st.markdown("## 📊 Library Summary")

summary_data = []

for doc in filtered_documents:

    summary_data.append({

        "Document": doc.get(
            "document_name"
        ),

        "Category": doc.get(
            "document_category"
        ),

        "Expiry Date": doc.get(
            "expiry_date"
        ),

        "Tags": doc.get(
            "tags"
        )
    })

summary_df = pd.DataFrame(
    summary_data
)

st.dataframe(

    summary_df,

    use_container_width=True
)
