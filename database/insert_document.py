from database.supabase_client import (
    supabase
)

# =====================================================
# INSERT DOCUMENT
# =====================================================

def insert_document(

    document_name,
    document_category,
    encrypted_path,
    ocr_text,
    tags,
    notes,
    expiry_date
):

    data = {

        "document_name": document_name,

        "document_category": document_category,

        "encrypted_path": encrypted_path,

        "ocr_text": ocr_text,

        "tags": tags,

        "notes": notes,

        "expiry_date": (
            str(expiry_date)
            if expiry_date
            else None
        )
    }

    response = (

        supabase
        .table("documents")
        .insert(data)
        .execute()
    )

    return response
