import re
from urllib.parse import urlparse


def clean_text(value):
    if value is None:
        return ""

    value = str(value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def clean_quote(value):
    value = clean_text(value)

    value = value.strip("“”\"'")

    return value.strip()


def clean_price(value):
    if value is None or value == "":
        return None

    value = str(value)

    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)

    if not match:
        return None

    return float(match.group())


def clean_rating(value):
    if value is None:
        return None

    value = clean_text(value).lower()

    ratings = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    if value.isdigit():
        number = int(value)
        return number if 1 <= number <= 5 else None

    return ratings.get(value)


def clean_tags(tags):
    if not tags:
        return []

    if isinstance(tags, str):
        tags = tags.split(",")

    cleaned_tags = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned_tags.append(tag)

    return cleaned_tags


def clean_url(value):
    if not value:
        return ""

    value = clean_text(value)

    parsed = urlparse(value)

    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value

    return ""