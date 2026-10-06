import csv
import json
import logging
from pathlib import Path

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes

from processing.cleaning import (
    clean_text,
    clean_quote,
    clean_price,
    clean_rating,
    clean_tags,
    clean_url,
)

from processing.validation import validate_record
from processing.deduplication import deduplicate_records


BOOKS_URL = "https://books.toscrape.com/"
QUOTES_URL = "https://quotes.toscrape.com/"

OUTPUT_DIR = Path("output")
LOG_DIR = Path("logs")

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def clean_record(record):
    """Convert a scraped record into the common data format."""

    cleaned = {
        "source": clean_text(record.get("source", "")),
        "title": clean_text(record.get("title", "")),
        "quote": clean_quote(record.get("quote", "")),
        "author": clean_text(record.get("author", "")),
        "price": clean_price(record.get("price")),
        "rating": clean_rating(record.get("rating")),
        "tags": clean_tags(record.get("tags", [])),
        "url": clean_url(record.get("url", "")),
        "author_url": clean_url(record.get("author_url", "")),
    }

    return cleaned


def write_csv(records):
    OUTPUT_DIR.mkdir(exist_ok=True)

    fieldnames = [
        "source",
        "title",
        "quote",
        "author",
        "price",
        "rating",
        "tags",
        "url",
        "author_url",
    ]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for record in records:
            row = record.copy()

            # Store tags as a readable string in CSV
            row["tags"] = ", ".join(record["tags"])

            writer.writerow(row)


def write_summary(summary):
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)


def main():
    setup_logging()

    print("Starting ETL pipeline...")
    logging.info("ETL pipeline started")

    # -------------------------
    # 1. Scraping
    # -------------------------

    try:
        books = scrape_books(BOOKS_URL)
        print(f"Books scraped: {len(books)}")
        logging.info("Books scraped: %d", len(books))
    except Exception as error:
        books = []
        print(f"Books scraper failed: {error}")
        logging.exception("Books scraper failed")

    try:
        quotes = scrape_quotes(QUOTES_URL)
        print(f"Quotes scraped: {len(quotes)}")
        logging.info("Quotes scraped: %d", len(quotes))
    except Exception as error:
        quotes = []
        print(f"Quotes scraper failed: {error}")
        logging.exception("Quotes scraper failed")

    all_records = books + quotes

    # -------------------------
    # 2. Cleaning
    # -------------------------

    cleaned_records = [
        clean_record(record)
        for record in all_records
    ]

    print(f"Records after cleaning: {len(cleaned_records)}")
    logging.info("Records cleaned: %d", len(cleaned_records))

    # -------------------------
    # 3. Validation
    # -------------------------

    valid_records = []
    rejected_records = []

    for record in cleaned_records:
        is_valid, reasons = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            rejected_records.append({
                "record": record,
                "reasons": reasons,
            })

    print(f"Valid records: {len(valid_records)}")
    print(f"Rejected records: {len(rejected_records)}")

    logging.info("Valid records: %d", len(valid_records))
    logging.info("Rejected records: %d", len(rejected_records))

    # -------------------------
    # 4. Deduplication
    # -------------------------

    unique_records = deduplicate_records(valid_records)

    duplicates_removed = (
        len(valid_records) - len(unique_records)
    )

    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final records: {len(unique_records)}")

    logging.info("Duplicates removed: %d", duplicates_removed)
    logging.info("Final records: %d", len(unique_records))

    # -------------------------
    # 5. Write CSV
    # -------------------------

    write_csv(unique_records)

    # -------------------------
    # 6. Write JSON summary
    # -------------------------

    summary = {
        "books_scraped": len(books),
        "quotes_scraped": len(quotes),
        "total_scraped": len(all_records),
        "valid_records": len(valid_records),
        "rejected_records": len(rejected_records),
        "duplicates_removed": duplicates_removed,
        "final_records": len(unique_records),
    }

    write_summary(summary)

    logging.info("CSV written to %s", CSV_FILE)
    logging.info("Summary written to %s", JSON_FILE)
    logging.info("ETL pipeline completed")

    print("\nETL pipeline completed successfully!")
    print(f"CSV: {CSV_FILE}")
    print(f"JSON: {JSON_FILE}")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()