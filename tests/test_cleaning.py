from processing.cleaning import (
    clean_text,
    clean_quote,
    clean_price,
    clean_rating,
    clean_tags,
    clean_url,
)


def test_clean_text():
    assert clean_text("   Hello    World   ") == "Hello World"


def test_clean_quote():
    assert clean_quote('  "Hello World"  ') == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_tags():
    assert clean_tags(["life", "inspiration"]) == ["life", "inspiration"]


def test_clean_url():
    assert clean_url("https://example.com") == "https://example.com"