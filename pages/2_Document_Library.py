import os
import traceback
import pandas as pd
import streamlit as st

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
# IMPORTS
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
# TEMP DIRECTORY
# =====================================================

os.makedirs(
    "temp_decrypted",
    exist_ok=True
)

# =====================================================
# PAGE TITLE
# =====================================================

st.markdown(
    """
    <div class='glass-card'>
        <h1>📚 Document Library</h1>
        <p>
            Browse, manage and securely access
            your encrypted documents.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

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
        "No documents available."
    )

    st.stop()

# =====================================================
# SEARCH + FILTERS
# =====================================================

st.markdown("## 🔍 Search & Filters")

col1, col2 = st.columns([3, 1])

with col1:

    search_query = st.text_input(
        "Search Documents",
        placeholder=(
            "Search by name, category, tags..."
        )
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

        "Filter Category",

        ["All"] + categories
    )

st.divider()

# =====================================================
# FILTER LOGIC
# =====================================================

filtered_documents = []

for row in documents:

    document_name = str(
        row.get(
            "document_name",
            ""
        )
    )

    document_category = str(
        row.get(
            "document_category",
            ""
        )
    )

    tags = str(
        row.get(
            "tags",
            ""
        )
    )

    combined_text = (

        document_name
        + " "
        + document_category
        + " "
        + tags

    ).lower()

    matches_search = (

        search_query.lower()
        in combined_text
    )

    matches_category = (

        selected_category == "All"

        or

        document_category
        == selected_category
    )

    if matches_search and matches_category:

        filtered_documents.append(row)

# =====================================================
# SUMMARY
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

        with st.container():

            st.markdown(
                "<div class='glass-card'>",
                unsafe_allow_html=True
            )

            # =========================================
            # DETAILS
            # =========================================

            col1, col2 = st.columns([4, 1])

            with col1:

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

                if row.get("notes"):

                    st.markdown(
                        f"**📝 Notes:** "
                        f"{row.get('notes')}"
                    )

                if row.get("expiry_date"):

                    st.markdown(
                        f"**📅 Expiry Date:** "
                        f"{row.get('expiry_date')}"
                    )

                if row.get("upload_date"):

                    st.markdown(
                        f"**⏱️ Uploaded:** "
                        f"{row.get('upload_date')}"
                    )

            # =========================================
            # ACTION BUTTONS
            # =========================================

            with col2:

                # =====================================
                # VIEW BUTTON
                # =====================================

                if st.button(

                    "👁️ View",

                    key=f"view_{row['id']}"
                ):

                    try:

                        encrypted_path = row.get(
                            "encrypted_path"
                        )

                        file_bytes = (

                            supabase.storage
                            .from_(
                                "encrypted-documents"
                            )
                            .download(
                                encrypted_path
                            )
                        )

                        temp_encrypted_path = os.path.join(

                            "temp_decrypted",

                            encrypted_path
                        )

                        with open(
                            temp_encrypted_path,
                            "wb"
                        ) as f:

                            f.write(file_bytes)

                        decrypted_output_path = os.path.join(

                            "temp_decrypted",

                            row.get(
                                "document_name"
                            )
                        )

                        decrypt_file(

                            temp_encrypted_path,

                            decrypted_output_path
                        )

                        with open(

                            decrypted_output_path,

                            "rb"

                        ) as file:

                            st.download_button(

                                label="⬇️ Download",

                                data=file,

                                file_name=row.get(
                                    "document_name"
                                ),

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

                # =====================================
                # EDIT BUTTON
                # =====================================

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

                # =====================================
                # DELETE BUTTON
                # =====================================

                if st.button(

                    "🗑️ Delete",

                    key=f"delete_{row['id']}"
                ):

                    try:

                        encrypted_path = row.get(
                            "encrypted_path"
                        )

                        # =============================
                        # DELETE FROM STORAGE
                        # =============================

                        if encrypted_path:

                            (
                                supabase.storage
                                .from_(
                                    "encrypted-documents"
                                )
                                .remove(
                                    [encrypted_path]
                                )
                            )

                        # =============================
                        # DELETE DATABASE RECORD
                        # =============================

                        (
                            supabase
                            .table("documents")
                            .delete()
                            .eq(
                                "id",
                                row["id"]
                            )
                            .execute()
                        )

                        st.success(
                            "Document deleted successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Delete failed: {e}"
                        )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
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

for row in filtered_documents:

    summary_data.append({

        "Document":
            row.get(
                "document_name"
            ),

        "Category":
            row.get(
                "document_category"
            ),

        "Expiry":
            row.get(
                "expiry_date"
            ),

        "Tags":
            row.get(
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
