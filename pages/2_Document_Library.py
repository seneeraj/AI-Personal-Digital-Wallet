import streamlit as st
import os

from sqlalchemy import select

from database.models import documents
from database.db_manager import engine

from database.delete_document import (
    delete_document
)

from modules.encryption.aes_decryptor import (
    decrypt_file
)

from security.auth_guard import (
    require_login
)

require_login()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Document Library",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📚 Document Library")

# =====================================================
# SEARCH
# =====================================================

search_query = st.text_input(
    "🔍 Search documents"
)

# =====================================================
# LOAD DOCUMENTS
# =====================================================

query = select(documents)

with engine.connect() as conn:

    results = conn.execute(query).fetchall()

# =====================================================
# FILTER DOCUMENTS
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

    ).lower()

    if search_query.lower() in searchable_text:

        filtered_results.append(row)

# =====================================================
# EMPTY STATE
# =====================================================

if not filtered_results:

    st.info("No documents found.")

# =====================================================
# DOCUMENT CARDS
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
            # DOCUMENT INFO
            # =====================================

            st.subheader(
                f"📄 {row.document_name}"
            )

            st.caption(
                f"📂 Category: {row.document_category}"
            )

            if row.tags:

                st.write(
                    f"🏷️ Tags: {row.tags}"
                )

            if row.notes:

                st.write(
                    f"📝 Notes: {row.notes}"
                )

            st.caption(
                f"📅 Uploaded: {row.upload_date}"
            )

            st.divider()

            # =====================================
            # BUTTONS
            # =====================================

            col1, col2, col3 = st.columns(3)

            # =====================================
            # VIEW
            # =====================================

            with col1:

                if st.button(
                    "👁 View",
                    key=f"view_{row.id}"
                ):

                    os.makedirs(
                        "temp_decrypted",
                        exist_ok=True
                    )

                    temp_output_path = os.path.join(

                        "temp_decrypted",

                        row.document_name
                    )

                    decrypt_file(

                        row.encrypted_path,

                        temp_output_path
                    )

                    # IMAGE
                    if row.document_name.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                    ):

                        st.image(
                            temp_output_path
                        )

                    # PDF
                    elif row.document_name.lower().endswith(
                        ".pdf"
                    ):

                        with open(
                            temp_output_path,
                            "rb"
                        ) as file:

                            st.download_button(

                                label="📥 Download PDF",

                                data=file,

                                file_name=row.document_name,

                                mime="application/pdf",

                                key=f"download_{row.id}"
                            )

            # =====================================
            # EDIT
            # =====================================

            with col2:

                if st.button(
                    "✏ Edit",
                    key=f"edit_{row.id}"
                ):

                    st.session_state[
                        "selected_document_id"
                    ] = row.id

                    st.switch_page(
                        "pages/3_Edit_Document.py"
                    )

            # =====================================
            # DELETE
            # =====================================

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{row.id}"
                ):

                    success, message = delete_document(

                        document_id=row.id,

                        encrypted_path=row.encrypted_path
                    )

                    if success:

                        st.success(message)

                        st.rerun()

                    else:

                        st.error(message)

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )
