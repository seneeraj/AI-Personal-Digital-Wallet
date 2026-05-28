from sqlalchemy import update

from database.models import documents
from database.db_manager import engine

def update_document_metadata(

    document_id,
    tags,
    notes
):

    try:

        query = update(documents).where(

            documents.c.id == document_id

        ).values(

            tags=tags,

            notes=notes
        )

        with engine.connect() as conn:

            conn.execute(query)

            conn.commit()

        return True

    except Exception:

        return False