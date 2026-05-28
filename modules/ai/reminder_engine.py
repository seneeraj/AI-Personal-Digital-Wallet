from datetime import datetime

def calculate_expiry_alert(
    expiry_date
):

    if not expiry_date:
        return None

    date_formats = [

        "%d/%m/%Y",

        "%d-%m-%Y"
    ]

    parsed_date = None

    # =============================================
    # TRY PARSING DATE
    # =============================================

    for fmt in date_formats:

        try:

            parsed_date = datetime.strptime(
                expiry_date,
                fmt
            )

            break

        except:

            continue

    if not parsed_date:
        return None

    # =============================================
    # CALCULATE DAYS LEFT
    # =============================================

    today = datetime.today()

    days_left = (
        parsed_date - today
    ).days

    # =============================================
    # GENERATE ALERTS
    # =============================================

    if days_left < 0:

        return (
            f"❌ Expired "
            f"{abs(days_left)} days ago"
        )

    elif days_left <= 30:

        return (
            f"🚨 Expiring in "
            f"{days_left} days"
        )

    elif days_left <= 180:

        return (
            f"⚠️ Expiring in "
            f"{days_left} days"
        )

    else:

        return (
            f"✅ Valid for "
            f"{days_left} more days"
        )