from sqlalchemy import insert

from datetime import datetime

from database.db_manager import engine
from database.models import documents

# =====================================================
# INSERT DOCUMENT
# =====================================================

def insert_document(

    document_name,
    document_category,
    encrypted_path,
    ocr_text="",
    tags="",
    notes="",
    expiry_date=None
):

    try:

        query = insert(documents).values(

            document_name=document_name,

            document_category=document_category,

            encrypted_path=encrypted_path,

            ocr_text=ocr_text,

            upload_date=datetime.now(),

            tags=tags,

            notes=notes,

            expiry_date=expiry_date
        )

        with engine.begin() as conn:

            conn.execute(query)

        return True

    except Exception as e:

        print(
            f"Insert document error: {e}"
        )

        return False