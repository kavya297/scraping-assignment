import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import create_session


def scrape_books(start_url):
    session = create_session()
    current_url = start_url
    results = []

    while current_url:
        response = session.get(current_url, timeout=10)
        response.raise_for_status()

        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        books = soup.select("article.product_pod")

        for book in books:
            title_element = book.select_one("h3 > a")
            title = title_element.get("title", "").strip()

            price_element = book.select_one("p.price_color")
            price = price_element.get_text(strip=True) if price_element else ""

            rating_element = book.select_one("p.star-rating")

            rating_classes = (
                rating_element.get("class", [])
                if rating_element
                else []
            )

            rating = (
                rating_classes[-1]
                if len(rating_classes) > 1
                else ""
            )

            relative_url = title_element.get("href", "")
            book_url = urljoin(current_url, relative_url)

            results.append({
                "source": "books",
                "title": title,
                "price": price,
                "rating": rating,
                "url": book_url,
            })

        # Find the next page dynamically
        next_link = soup.select_one("li.next > a")

        if next_link:
            next_url = next_link.get("href", "")
            current_url = urljoin(current_url, next_url)
        else:
            current_url = None

        # Required delay between requests
        time.sleep(0.5)

    return results


if __name__ == "__main__":
    print("Testing books scraper...")

    url = "https://books.toscrape.com/"
    books = scrape_books(url)

    print("Number of books:", len(books))
    print(books[0])