from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import os

# =====================================================
# KEY FILE LOCATION
# =====================================================

KEY_FILE = "security/master.key"

# =====================================================
# GENERATE AES-256 KEY
# =====================================================

def generate_key():

    os.makedirs(
        "security",
        exist_ok=True
    )

    if not os.path.exists(KEY_FILE):

        key = get_random_bytes(32)

        with open(KEY_FILE, "wb") as f:
            f.write(key)

# =====================================================
# LOAD AES KEY
# =====================================================

def load_key():

    if not os.path.exists(KEY_FILE):
        generate_key()

    with open(KEY_FILE, "rb") as f:
        return f.read()

# =====================================================
# ENCRYPT FILE
# =====================================================

def encrypt_file(
    input_file,
    output_file
):

    key = load_key()

    # Create AES cipher
    cipher = AES.new(
        key,
        AES.MODE_EAX
    )

    # Read original file
    with open(input_file, "rb") as f:
        file_data = f.read()

    # Encrypt data
    ciphertext, tag = cipher.encrypt_and_digest(
        file_data
    )

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    # Save encrypted file
    with open(output_file, "wb") as f:

        # Save nonce
        f.write(cipher.nonce)

        # Save tag
        f.write(tag)

        # Save encrypted data
        f.write(ciphertext)

# =====================================================
# OPTIONAL HELPER
# =====================================================

def file_exists(filepath):

    return os.path.exists(filepath)