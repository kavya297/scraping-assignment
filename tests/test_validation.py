from processing.validation import validate_record


def test_valid_book():
    record = {
        "source": "books",
        "title": "A Good Book",
        "price": 25.50,
        "rating": 4,
        "url": "https://books.toscrape.com/"
    }

    is_valid, reasons = validate_record(record)

    assert is_valid is True
    assert reasons == []


def test_invalid_rating():
    record = {
        "source": "books",
        "title": "A Good Book",
        "price": 25.50,
        "rating": 7,
        "url": "https://books.toscrape.com/"
    }

    is_valid, reasons = validate_record(record)

    assert is_valid is False
    assert "Rating must be between 1 and 5" in reasons


def test_missing_title():
    record = {
        "source": "books",
        "title": "",
        "price": 25.50,
        "rating": 4,
        "url": "https://books.toscrape.com/"
    }

    is_valid, reasons = validate_record(record)

    assert is_valid is False
    assert "Missing title or quote" in reasons