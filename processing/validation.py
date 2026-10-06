from urllib.parse import urlparse


ALLOWED_SOURCES = {"books", "quotes"}


def validate_record(record):
    reasons = []

    # Check source
    if record.get("source") not in ALLOWED_SOURCES:
        reasons.append("Invalid source")

    # Check title/name/quote
    title = record.get("title", "")
    quote = record.get("quote", "")

    if not title and not quote:
        reasons.append("Missing title or quote")

    # Check URL
    url = record.get("url", "")

    if url:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https"):
            reasons.append("Invalid URL")
    else:
        reasons.append("Missing URL")

    # Check price
    price = record.get("price")

    if price is not None:
        try:
            if float(price) < 0:
                reasons.append("Price cannot be negative")
        except (ValueError, TypeError):
            reasons.append("Invalid price")

    # Check rating
    rating = record.get("rating")

    if rating is not None:
        try:
            rating = int(rating)

            if rating < 1 or rating > 5:
                reasons.append("Rating must be between 1 and 5")

        except (ValueError, TypeError):
            reasons.append("Invalid rating")

    return len(reasons) == 0, reasons