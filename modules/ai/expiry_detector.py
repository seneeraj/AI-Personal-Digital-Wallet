import re
from datetime import datetime

# =====================================================
# DETECT EXPIRY DATE
# =====================================================

def detect_expiry_date(text):

    if not text:

        return None

    # =============================================
    # FIND DATE PATTERNS
    # =============================================

    date_patterns = [

        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}-\d{2}-\d{4}",
        r"\d{4}-\d{2}-\d{2}"
    ]

    found_dates = []

    for pattern in date_patterns:

        matches = re.findall(pattern, text)

        found_dates.extend(matches)

    # =============================================
    # PARSE DATES
    # =============================================

    parsed_dates = []

    for date_str in found_dates:

        for fmt in (

            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d"
        ):

            try:

                parsed_date = datetime.strptime(
                    date_str,
                    fmt
                )

                parsed_dates.append(
                    parsed_date
                )

            except:
                pass

    # =============================================
    # FUTURE DATES ONLY
    # =============================================

    future_dates = [

        d for d in parsed_dates

        if d > datetime.now()
    ]

    # =============================================
    # RETURN LATEST DATE
    # =============================================

    if future_dates:

        latest_date = max(future_dates)

        return latest_date.strftime(
            "%Y-%m-%d"
        )

    return None