from database.db_manager import engine
from database.models import metadata

def initialize_database():

    metadata.create_all(engine)