# Realisieren Technologies - Web Scraping ETL Assignment

## Overview

This project is a Python-based ETL web scraping application that collects data from two practice websites:

- Books to Scrape
- Quotes to Scrape

The scraped data is cleaned, validated, deduplicated, consolidated, and exported into a CSV file. A JSON summary report and application log are also generated.

## Technologies Used

- Python 3.12
- Requests
- BeautifulSoup4
- lxml
- Pytest
- CSV
- JSON
- Logging

## Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md