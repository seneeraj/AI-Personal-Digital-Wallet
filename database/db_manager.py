from sqlalchemy import create_engine

import os

# =====================================================
# CREATE RUNTIME DATABASE DIRECTORY
# =====================================================

os.makedirs(
    "/tmp/ai_vault_db",
    exist_ok=True
)

# =====================================================
# DATABASE PATH
# =====================================================

DATABASE_PATH = (
    "/tmp/ai_vault_db/vault.db"
)

# =====================================================
# SQLALCHEMY ENGINE
# =====================================================

engine = create_engine(

    f"sqlite:///{DATABASE_PATH}",

    connect_args={
        "check_same_thread": False
    }
)
