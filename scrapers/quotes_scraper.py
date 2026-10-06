import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import create_session


def scrape_quotes(start_url):
    session = create_session()
    current_url = start_url
    results = []

    while current_url:
        response = session.get(current_url, timeout=10)
        response.raise_for_status()

        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        quotes = soup.select("div.quote")

        for quote in quotes:
            quote_element = quote.select_one("span.text")
            quote_text = quote_element.get_text(strip=True) if quote_element else ""

            author_element = quote.select_one("small.author")
            author = author_element.get_text(strip=True) if author_element else ""

            tag_elements = quote.select("div.tags a.tag")
            tags = [tag.get_text(strip=True) for tag in tag_elements]

            author_url = ""
            if author_element:
                author_link = author_element.parent.select_one("a")
                if author_link:
                    author_url = urljoin(current_url, author_link.get("href", ""))

            results.append({
                "source": "quotes",
                "quote": quote_text,
                "author": author,
                "tags": tags,
                "author_url": author_url,
                "url": current_url,
            })

        next_link = soup.select_one("li.next > a")

        if next_link:
            next_url = next_link.get("href")
            current_url = urljoin(current_url, next_url)
        else:
            current_url = None

        time.sleep(0.5)

    return results


if __name__ == "__main__":
    print("Testing quotes scraper...")

    url = "https://quotes.toscrape.com/"
    quotes = scrape_quotes(url)

    print("Number of quotes:", len(quotes))
    print(quotes[0])