from processing.deduplication import deduplicate_records


def test_duplicate_books_are_removed():
    records = [
        {"source": "books", "title": "The Great Book"},
        {"source": "books", "title": "the great book"},
        {"source": "books", "title": "Another Book"},
    ]

    result = deduplicate_records(records)

    assert len(result) == 2