import os
import uuid
import traceback

import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Upload Documents",
    page_icon="⬆️",
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
# CREATE REQUIRED FOLDERS
# =====================================================

os.makedirs(
    "uploads/temp",
    exist_ok=True
)

os.makedirs(
    "encrypted_storage",
    exist_ok=True
)

os.makedirs(
    "temp_decrypted",
    exist_ok=True
)

# =====================================================
# IMPORT MODULES
# =====================================================

from modules.uploads.upload_handler import (
    save_temp_file
)

from modules.ocr.ocr_engine import (
    extract_text_from_file
)

from modules.ai.document_classifier import (
    classify_document
)

from modules.ai.tag_generator import (
    generate_tags
)

from modules.ai.expiry_detector import (
    detect_expiry_date
)

from modules.encryption.aes_encryptor import (
    encrypt_file
)

from modules.storage.supabase_storage import (
    upload_encrypted_file
)

from database.insert_document import (
    insert_document
)

# =====================================================
# SESSION STATE
# =====================================================

if "upload_completed" not in st.session_state:

    st.session_state[
        "upload_completed"
    ] = False

# =====================================================
# PAGE TITLE
# =====================================================

st.title("⬆️ Upload Documents")

st.caption(
    "Securely upload and encrypt your files."
)

st.divider()

# =====================================================
# SUCCESS MESSAGE
# =====================================================

if st.session_state[
    "upload_completed"
]:

    st.success(
        "✅ Document uploaded successfully."
    )

    st.session_state[
        "upload_completed"
    ] = False

# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_files = st.file_uploader(

    "Drag and drop documents here",

    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "docx"
    ],

    accept_multiple_files=True
)

# =====================================================
# CATEGORY
# =====================================================

category = st.selectbox(

    "📁 Select Default Category",

    [
        "Personal",
        "Financial",
        "Medical",
        "Educational",
        "Legal",
        "Other"
    ]
)

# =====================================================
# TAGS
# =====================================================

user_tags = st.text_input(

    "🏷️ Additional Tags (comma separated)",

    placeholder="identity, passport, govt"
)

# =====================================================
# NOTES
# =====================================================

user_notes = st.text_area(

    "📝 Notes",

    placeholder="Optional notes..."
)

st.divider()

# =====================================================
# UPLOAD BUTTON
# =====================================================

if st.button("🚀 Upload Documents"):

    # =================================================
    # VALIDATION
    # =================================================

    if not uploaded_files:

        st.warning(
            "Please upload at least one document."
        )

    else:

        # =============================================
        # PROCESS FILES
        # =============================================

        for uploaded_file in uploaded_files:

            try:

                with st.spinner(

                    f"Processing {uploaded_file.name}..."
                ):

                    # =================================
                    # SAVE TEMP FILE
                    # =================================

                    temp_path = save_temp_file(
                        uploaded_file
                    )

                    # =================================
                    # OCR EXTRACTION
                    # =================================

                    try:

                        ocr_text = (
                            extract_text_from_file(
                                temp_path
                            )
                        )

                    except Exception:

                        ocr_text = ""

                    # =================================
                    # AI CATEGORY
                    # =================================

                    try:

                        ai_category = (
                            classify_document(
                                ocr_text
                            )
                        )

                    except Exception:

                        ai_category = category

                    final_category = (

                        ai_category
                        if ai_category
                        else category
                    )

                    # =================================
                    # AI TAGS
                    # =================================

                    try:

                        ai_tags = generate_tags(
                            ocr_text
                        )

                    except Exception:

                        ai_tags = []

                    # =================================
                    # USER TAGS
                    # =================================

                    manual_tags = [

                        tag.strip()

                        for tag in user_tags.split(",")

                        if tag.strip()
                    ]

                    # =================================
                    # COMBINED TAGS
                    # =================================

                    combined_tags = list(

                        set(
                            ai_tags + manual_tags
                        )
                    )

                    combined_tags = ",".join(
                        combined_tags
                    )

                    # =================================
                    # EXPIRY DATE
                    # =================================

                    try:

                        detected_expiry = (
                            detect_expiry_date(
                                ocr_text
                            )
                        )

                    except Exception:

                        detected_expiry = None

                    # =================================
                    # UNIQUE ENCRYPTED FILENAME
                    # =================================

                    unique_filename = str(
                        uuid.uuid4()
                    )

                    # =================================
                    # LOCAL ENCRYPTED FILE PATH
                    # =================================

                    encrypted_path = os.path.join(

                        "encrypted_storage",

                        unique_filename + ".enc"
                    )

                    # =================================
                    # ENCRYPT FILE
                    # =================================

                    encrypt_file(

                        temp_path,

                        encrypted_path
                    )

                    # =================================
                    # UPLOAD TO SUPABASE STORAGE
                    # =================================

                    upload_response = (
                        upload_encrypted_file(

                            encrypted_path,

                            unique_filename + ".enc"
                        )
                    )

                    # =================================
                    # VERIFY STORAGE UPLOAD
                    # =================================

                    if upload_response is None:

                        st.error(
                            f"❌ Storage upload failed for "
                            f"{uploaded_file.name}"
                        )

                        continue

                    # =================================
                    # SAVE METADATA TO SUPABASE
                    # =================================

                    insert_document(

                        document_name=uploaded_file.name,

                        document_category=final_category,

                        encrypted_path=(
                            unique_filename + ".enc"
                        ),

                        ocr_text=ocr_text,

                        tags=combined_tags,

                        notes=user_notes,

                        expiry_date=detected_expiry
                    )

                    # =================================
                    # DELETE TEMP FILES
                    # =================================

                    if os.path.exists(temp_path):

                        os.remove(temp_path)

                    # =================================
                    # OPTIONAL LOCAL CLEANUP
                    # =================================

                    # if os.path.exists(
                    #     encrypted_path
                    # ):
                    #
                    #     os.remove(
                    #         encrypted_path
                    #     )

                # =====================================
                # SUCCESS FLAG
                # =====================================

                st.session_state[
                    "upload_completed"
                ] = True

            except Exception as e:

                st.error(
                    f"❌ Error uploading "
                    f"{uploaded_file.name}: {e}"
                )

                st.code(
                    traceback.format_exc()
                )
