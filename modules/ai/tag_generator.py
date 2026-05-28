def generate_tags(
    ocr_text,
    category
):

    text = ocr_text.lower()

    tags = []

    # =============================================
    # CATEGORY TAGS
    # =============================================

    tags.append(category.lower())

    # =============================================
    # COMMON TAGS
    # =============================================

    keyword_mapping = {

        "aadhaar": "identity",

        "passport": "travel",

        "pan": "tax",

        "insurance": "policy",

        "bank": "finance",

        "hospital": "health",

        "doctor": "medical",

        "university": "education",

        "degree": "qualification",

        "court": "legal"
    }

    for keyword, tag in keyword_mapping.items():

        if keyword in text:
            tags.append(tag)

    # Remove duplicates
    tags = list(set(tags))

    return ", ".join(tags)