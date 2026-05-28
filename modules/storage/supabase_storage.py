import streamlit as st

from database.supabase_client import (
    supabase
)

# =====================================================
# UPLOAD ENCRYPTED FILE
# =====================================================

def upload_encrypted_file(

    local_file_path,
    storage_filename
):

    try:

        # =============================================
        # READ FILE
        # =============================================

        with open(
            local_file_path,
            "rb"
        ) as f:

            file_data = f.read()

        # =============================================
        # UPLOAD TO SUPABASE
        # =============================================

        response = (

            supabase.storage
            .from_("encrypted-documents")
            .upload(

                storage_filename,

                file_data
            )
        )

        st.success(
            f"Uploaded to storage: "
            f"{storage_filename}"
        )

        return response

    except Exception as e:

        st.error(
            f"Storage upload failed: {e}"
        )

        return None
