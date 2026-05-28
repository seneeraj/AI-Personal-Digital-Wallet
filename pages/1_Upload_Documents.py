import streamlit as st
import os
import uuid

from modules.encryption.aes_encryptor import (
    encrypt_file
)

from modules.ocr.ocr_engine import (

    extract_text_from_image,

    extract_text_from_pdf
)

from modules.ai.document_classifier import (
    classify_document
)

from modules.ai.expiry_detector import (
    detect_expiry_date
)

from database.insert_document import (
    insert_document
)

from security.auth_guard import (
    require_login
)

from modules.storage.supabase_storage import (
    upload_encrypted_file
)


require_login()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Upload Documents",
    page_icon="⬆️",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("⬆️ Upload Documents")

st.caption(
    "Securely upload and encrypt your files."
)

st.divider()

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
# CATEGORY SELECTION
# =====================================================

categories = [

    "Personal",
    "Financial",
    "Medical",
    "Education",
    "Legal",
    "Uncategorized"
]

selected_category = st.selectbox(

    "📂 Select Default Category",

    categories
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

    placeholder="Optional notes about document",

    height=120
)

st.divider()

# =====================================================
# UPLOAD BUTTON
# =====================================================

if st.button("🚀 Upload Documents"):

    if not uploaded_files:

        st.warning(
            "Please upload at least one file."
        )

    else:

        progress_bar = st.progress(0)

        total_files = len(uploaded_files)

        # =============================================
        # CREATE REQUIRED FOLDERS
        # =============================================

        os.makedirs(
            "uploads/temp",
            exist_ok=True
        )

        os.makedirs(
            "encrypted_storage",
            exist_ok=True
        )

        # =============================================
        # PROCESS FILES
        # =============================================

        for index, uploaded_file in enumerate(uploaded_files):

            try:

                # =====================================
                # UNIQUE FILE NAME
                # =====================================

                unique_name = (

                    str(uuid.uuid4())
                    + "_"
                    + uploaded_file.name
                )

                # =====================================
                # TEMP FILE PATH
                # =====================================

                temp_path = os.path.join(

                    "uploads/temp",

                    unique_name
                )

                # =====================================
                # SAVE TEMP FILE
                # =====================================

                with open(temp_path, "wb") as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                # =====================================
                # OCR EXTRACTION
                # =====================================

                ocr_text = ""

                # =====================================
                # IMAGE OCR
                # =====================================

                if uploaded_file.name.lower().endswith(

                    (".png", ".jpg", ".jpeg")

                ):

                    ocr_text = extract_text_from_image(
                        temp_path
                    )

                # =====================================
                # PDF TEXT EXTRACTION
                # =====================================

                elif uploaded_file.name.lower().endswith(
                    ".pdf"
                ):

                    ocr_text = extract_text_from_pdf(
                        temp_path
                    )

                # =====================================
                # AI CLASSIFICATION
                # =====================================

                ai_category, ai_tags = classify_document(
                    ocr_text
                )

                # =====================================
                # EXPIRY DETECTION
                # =====================================

                detected_expiry = detect_expiry_date(
                    ocr_text
                )

                # =====================================
                # FINAL CATEGORY
                # =====================================

                final_category = (

                    ai_category

                    if ai_category != "Uncategorized"

                    else selected_category
                )

                # =====================================
                # COMBINE TAGS
                # =====================================

                user_tags_list = [

                    tag.strip()

                    for tag in user_tags.split(",")

                    if tag.strip()
                ]

                combined_tags = ", ".join(

                    list(
                        set(
                            ai_tags
                            + user_tags_list
                        )
                    )
                )

                # =====================================
                # ENCRYPTED FILE NAME
                # =====================================

                encrypted_filename = (
                    uploaded_file.name
                    + ".enc"
                )

                encrypted_path = os.path.join(

                    "encrypted_storage",

                    encrypted_filename
                )

                # =====================================
                # ENCRYPT FILE
                # =====================================

                encrypt_file(

                    temp_path,

                    encrypted_path
                )

                # =============================================
                # UPLOAD ENCRYPTED FILE TO SUPABASE
                # =============================================

                upload_encrypted_file(

                    encrypted_path,

                    unique_filename + ".enc"
                )




                # =====================================
                # SAVE TO DATABASE
                # =====================================

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

                # =====================================
                # REMOVE TEMP FILE
                # =====================================

                if os.path.exists(temp_path):

                    os.remove(temp_path)

                # =====================================
                # PROGRESS BAR
                # =====================================

                progress = int(

                    ((index + 1) / total_files)
                    * 100
                )

                progress_bar.progress(progress)

                # =====================================
                # SUCCESS MESSAGE
                # =====================================

                st.success(
                    f"✅ Uploaded: "
                    f"{uploaded_file.name}"
                )

                # =====================================
                # INFO MESSAGE
                # =====================================

                info_message = f"""
📂 Category: {final_category}

🏷️ Tags: {combined_tags}
"""

                if detected_expiry:

                    info_message += (
                        f"\n\n📅 Expiry Detected: "
                        f"{detected_expiry}"
                    )

                st.info(info_message)

            except Exception as e:

                st.error(

                    f"❌ Error uploading "

                    f"{uploaded_file.name}: {e}"
                )

        st.success(
            "🎉 All documents uploaded successfully."
        )

        st.info(
            "Files encrypted and stored securely."
        )
