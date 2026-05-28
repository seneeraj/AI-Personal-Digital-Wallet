from Crypto.Cipher import AES
import os

KEY_FILE = "security/master.key"

# Load encryption key
def load_key():

    with open(KEY_FILE, "rb") as f:
        return f.read()

# Decrypt file
def decrypt_file(
    encrypted_file,
    output_file
):

    key = load_key()

    with open(encrypted_file, "rb") as f:

        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(
        key,
        AES.MODE_EAX,
        nonce=nonce
    )

    data = cipher.decrypt_and_verify(
        ciphertext,
        tag
    )

    with open(output_file, "wb") as f:
        f.write(data)