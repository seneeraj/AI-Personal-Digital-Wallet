# 🔐 AI Personal Digital Vault

AI Personal Digital Vault is an AI-powered secure personal document intelligence system built with Streamlit and Python.

The application allows users to:

* Securely upload personal documents
* Encrypt sensitive files
* Perform OCR-based text extraction
* Automatically classify documents using AI
* Generate smart tags
* Detect expiry dates
* Search documents intelligently
* Manage metadata
* Track reminders and expiry alerts

---

# 🚀 Features

## ✅ Secure Vault Authentication

* Master password protection
* Vault lock/unlock system
* Session-based access control

---

## ✅ AI-Powered Document Intelligence

The application automatically:

* Detects document categories
* Generates tags
* Extracts OCR text
* Detects expiry dates
* Enables intelligent search

Supported document types:

* PAN Card
* Aadhaar Card
* Passport
* Driving License
* Medical Reports
* Financial Documents
* Educational Certificates
* Legal Documents

---

# 🔒 Security Features

## AES Encryption

All uploaded documents are encrypted before storage.

## Temporary Decryption

Files are decrypted only temporarily during viewing/downloading.

## Secure Storage

Encrypted files are stored separately from application logic.

---

# 🧠 AI Features

## OCR Extraction

Supports:

* Image OCR
* PDF text extraction

## AI Classification

Automatically detects:

* Personal documents
* Financial documents
* Medical reports
* Educational certificates
* Legal documents

## Smart Tagging

Automatically generates contextual tags.

## Expiry Detection

Automatically detects:

* Passport expiry
* Driving license expiry
* Insurance expiry
* Visa expiry

---

# 🔍 Smart Search

The Smart Search module supports:

* Filename search
* OCR text search
* Tag search
* Notes search
* Category filtering

Examples:

```text
passport
medical report
income tax
hospital
bank statement
```

---

# 📅 Smart Alerts & Reminders

Dashboard automatically displays:

* Expired documents
* Expiring soon documents
* Valid documents
* Remaining validity days

---

# 🖥️ Technology Stack

## Frontend

* Streamlit

## Backend

* Python
* SQLAlchemy
* SQLite

## AI & OCR

* Tesseract OCR
* PyMuPDF

## Security

* AES Encryption
* Password Hashing

---

# 📂 Project Structure

```text
AI_Digital_Vault/
│
├── Dashboard.py
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── style.css
│
├── pages/
│   ├── 1_Upload_Documents.py
│   ├── 2_Document_Library.py
│   ├── 4_Search.py
│   └── internal/
│       └── 3_Edit_Document.py
│
├── database/
│   ├── db_manager.py
│   ├── delete_document.py
│   ├── document_manager.py
│   ├── insert_document.py
│   ├── models.py
│   ├── update_category.py
│   └── update_metadata.py
│
├── modules/
│   ├── ai/
│   │   ├── document_classifier.py
│   │   ├── expiry_detector.py
│   │   ├── reminder_engine.py
│   │   └── tag_generator.py
│   │
│   ├── encryption/
│   │   ├── aes_encryptor.py
│   │   └── aes_decryptor.py
│   │
│   ├── ocr/
│   │   └── ocr_engine.py
│   │
│   └── uploads/
│       ├── file_validator.py
│       └── upload_handler.py
│
└── security/
    ├── encryption_key.py
    ├── master_auth.py
    └── session_manager.py
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <repository_url>
```

---

## 2️⃣ Open Project

```bash
cd AI_Digital_Vault
```

---

## 3️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run Dashboard.py
```

---

# 🔧 Required Dependencies

Core packages:

```text
streamlit
sqlalchemy
pillow
pytesseract
pymupdf
cryptography
pandas
```

---

# 🔐 Security Notes

The following files/folders must NOT be uploaded publicly:

```text
venv/
database/db.sqlite3
security/master.hash
security/master.key
encrypted_storage/
temp_decrypted/
uploads/temp/
```

---

# 📄 Recommended .gitignore

```text
# Python
__pycache__/
*.pyc

# Virtual Environment
venv/

# Database
*.db
*.sqlite3

# Security
security/master.hash
security/master.key

# Encrypted Files
encrypted_storage/

# Temp Files
uploads/temp/
temp_decrypted/

# Logs
logs/

# OS
.DS_Store
Thumbs.db
```

---

# 🚀 Future Roadmap

## Planned Features

* Semantic AI Search
* AI Chat with Documents
* Email Alerts
* Cloud Storage Integration
* Multi-user Vaults
* Role-based Access
* Mobile App
* Voice Search
* Document Sharing
* AI Summarization

---

# 📸 Application Modules

## Dashboard

* Vault statistics
* Recent uploads
* Expiry alerts
* Quick actions

## Upload Documents

* Multi-file upload
* OCR extraction
* AI categorization
* Encryption

## Document Library

* View documents
* Edit metadata
* Delete documents
* Manage categories

## Smart Search

* OCR search
* Intelligent filtering
* Category search
* Metadata search

---

# 🧪 Tested Document Types

* JPG
* JPEG
* PNG
* PDF
* DOCX

---

# 👨‍💻 Developer Notes

This project is designed as:

* A secure personal AI document wallet
* A modular Streamlit architecture
* A production-style AI document management system

---

# 📜 License

This project is licensed under the MIT License.

---

# 🙌 Acknowledgements

Built using:

* Streamlit
* SQLAlchemy
* Tesseract OCR
* PyMuPDF
* Python

---

# ⭐ AI Digital Vault

An intelligent, secure, AI-powered personal document management platform.
