import os

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

        with open(
            local_file_path,
            "rb"
        ) as f:

            file_data = f.read()

        response = (

            supabase.storage
            .from_("encrypted-documents")
            .upload(

                storage_filename,

                file_data
            )
        )

        return response

    except Exception as e:

        print(e)

        return None
