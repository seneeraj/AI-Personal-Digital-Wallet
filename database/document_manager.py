from sqlalchemy import insert

from database.models import documents
from database.db_manager import engine

def save_document_metadata(

    document_name,
    category,
    encrypted_path,
    ocr_text,
    upload_date,
    tags="",
    notes="",
    expiry_date=""
):

    query = insert(documents).values(

        document_name=document_name,

        document_category=category,

        encrypted_path=encrypted_path,

        ocr_text=ocr_text,

        upload_date=upload_date,

        tags=tags,

        notes=notes,

        expiry_date=expiry_date
    )

    with engine.connect() as conn:

        conn.execute(query)

        conn.commit()