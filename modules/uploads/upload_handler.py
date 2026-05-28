import os
import uuid

TEMP_UPLOAD_DIR = "uploads/temp"

# Auto-create folder
os.makedirs(
    TEMP_UPLOAD_DIR,
    exist_ok=True
)

def save_temp_file(uploaded_file):

    unique_filename = (
        str(uuid.uuid4())
        + "_"
        + uploaded_file.name
    )

    filepath = os.path.join(
        TEMP_UPLOAD_DIR,
        unique_filename
    )

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath