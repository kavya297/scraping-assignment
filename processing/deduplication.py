import hashlib
import re
import string


def normalize_text(value):
    """Normalize text for duplicate comparison."""
    value = str(value).lower().strip()

    value = value.translate(
        str.maketrans("", "", string.punctuation)
    )

    value = re.sub(r"\s+", " ", value)

    return value


def create_fingerprint(record):
    """Create a unique fingerprint for a record."""

    source = record.get("source", "")

    if source == "books":
        text = normalize_text(record.get("title", ""))

    elif source == "quotes":
        quote = normalize_text(record.get("quote", ""))
        author = normalize_text(record.get("author", ""))

        text = author + "|" + quote[:50]

    else:
        text = str(record)

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def deduplicate_records(records):
    """Remove duplicate records using fingerprints."""

    unique_records = []
    seen = set()

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_records.append(record)

    return unique_records