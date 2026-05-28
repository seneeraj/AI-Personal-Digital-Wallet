ALLOWED_EXTENSIONS = [
    "pdf",
    "png",
    "jpg",
    "jpeg"
]

MAX_FILE_SIZE_MB = 10

def validate_file(uploaded_file):

    filename = uploaded_file.name

    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Unsupported file type"

    file_size_mb = (
        uploaded_file.size / (1024 * 1024)
    )

    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, "File too large"

    return True, "Valid file"