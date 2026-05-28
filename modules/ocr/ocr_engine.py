import fitz
import pytesseract

from PIL import Image

# =====================================================
# OCR FROM IMAGE
# =====================================================

def extract_text_from_image(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image
        )

        return text

    except Exception as e:

        print(e)

        return ""

# =====================================================
# TEXT EXTRACTION FROM PDF
# =====================================================

def extract_text_from_pdf(pdf_path):

    try:

        doc = fitz.open(pdf_path)

        full_text = ""

        for page in doc:

            full_text += page.get_text()

        return full_text

    except Exception as e:

        print(e)

        return ""

# =====================================================
# UNIVERSAL FILE TEXT EXTRACTION
# =====================================================

def extract_text_from_file(file_path):

    try:

        file_path_lower = file_path.lower()

        # =============================================
        # IMAGE FILES
        # =============================================

        if file_path_lower.endswith(

            (
                ".png",
                ".jpg",
                ".jpeg"
            )
        ):

            return extract_text_from_image(
                file_path
            )

        # =============================================
        # PDF FILES
        # =============================================

        elif file_path_lower.endswith(
            ".pdf"
        ):

            return extract_text_from_pdf(
                file_path
            )

        # =============================================
        # DOCX SUPPORT
        # =============================================

        elif file_path_lower.endswith(
            ".docx"
        ):

            return ""

        # =============================================
        # UNSUPPORTED FILES
        # =============================================

        return ""

    except Exception as e:

        print(e)

        return ""
