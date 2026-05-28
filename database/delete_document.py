import os

from sqlalchemy import delete

from database.models import documents
from database.db_manager import engine

def delete_document(
    document_id,
    encrypted_path
):

    try:

        # -----------------------------------------
        # Delete encrypted file
        # -----------------------------------------

        if os.path.exists(encrypted_path):

            os.remove(encrypted_path)

        # -----------------------------------------
        # Delete DB record
        # -----------------------------------------

        query = delete(documents).where(
            documents.c.id == document_id
        )

        with engine.connect() as conn:

            conn.execute(query)

            conn.commit()

        return True, "Document deleted successfully."

    except Exception as e:

        return False, str(e)