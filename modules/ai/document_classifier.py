import re

# =====================================================
# AI DOCUMENT CLASSIFIER
# =====================================================

def classify_document(text):

    if not text:

        return (
            "Uncategorized",
            []
        )

    text = text.lower()

    # =============================================
    # PAN CARD
    # =============================================

    if (

        "income tax department" in text
        or "permanent account number" in text
        or re.search(
            r"[A-Z]{5}[0-9]{4}[A-Z]",
            text.upper()
        )
    ):

        return (

            "Personal",

            [
                "pan",
                "identity",
                "government",
                "tax"
            ]
        )

    # =============================================
    # AADHAAR
    # =============================================

    if (

        "aadhaar" in text
        or "uidai" in text
    ):

        return (

            "Personal",

            [
                "aadhaar",
                "identity",
                "government"
            ]
        )

    # =============================================
    # PASSPORT
    # =============================================

    if "passport" in text:

        return (

            "Personal",

            [
                "passport",
                "travel",
                "identity"
            ]
        )

    # =============================================
    # MEDICAL
    # =============================================

    medical_keywords = [

        "hospital",
        "diagnosis",
        "prescription",
        "patient",
        "doctor",
        "medical"
    ]

    if any(
        word in text
        for word in medical_keywords
    ):

        return (

            "Medical",

            [
                "medical",
                "health",
                "hospital"
            ]
        )

    # =============================================
    # FINANCIAL
    # =============================================

    financial_keywords = [

        "bank",
        "statement",
        "account",
        "ifsc",
        "transaction",
        "balance"
    ]

    if any(
        word in text
        for word in financial_keywords
    ):

        return (

            "Financial",

            [
                "bank",
                "finance",
                "statement"
            ]
        )

    # =============================================
    # EDUCATION
    # =============================================

    education_keywords = [

        "university",
        "marksheet",
        "certificate",
        "degree",
        "education"
    ]

    if any(
        word in text
        for word in education_keywords
    ):

        return (

            "Education",

            [
                "education",
                "certificate",
                "academic"
            ]
        )

    # =============================================
    # DEFAULT
    # =============================================

    return (

        "Uncategorized",

        [
            "document"
        ]
    )