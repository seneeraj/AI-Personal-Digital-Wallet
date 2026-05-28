import pytesseract
import fitz

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