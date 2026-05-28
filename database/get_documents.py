from database.supabase_client import (
    supabase
)

# =====================================================
# GET ALL DOCUMENTS
# =====================================================

def get_all_documents():

    response = (

        supabase
        .table("documents")
        .select("*")
        .order(
            "upload_date",
            desc=True
        )
        .execute()
    )

    return response.data