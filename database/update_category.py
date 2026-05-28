from sqlalchemy import update

from database.models import documents
from database.db_manager import engine

def update_document_category(

    document_id,
    new_category
):

    try:

        query = update(documents).where(

            documents.c.id == document_id

        ).values(

            document_category=new_category
        )

        # =========================================
        # EXECUTE + COMMIT
        # =========================================

        with engine.begin() as conn:

            conn.execute(query)

        return True

    except Exception as e:

        print(e)

        return False