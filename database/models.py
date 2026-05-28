from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    MetaData
)

from database.db_manager import engine

metadata = MetaData()

# Vault Configuration Table
vault_config = Table(
    "vault_config",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "master_password_hash",
        String
    )
)

# Documents Table
documents = Table(
    "documents",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "document_name",
        String
    ),

    Column(
        "document_category",
        String
    ),

    Column(
        "encrypted_path",
        String
    ),

    Column(
        "ocr_text",
        Text
    ),

    Column(
        "upload_date",
        String
    ),
    Column("tags", Text),

    Column("notes", Text),
    
    Column("expiry_date", String),
)

# Create tables
metadata.create_all(engine)