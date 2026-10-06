import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonScraper/1.0"
    })

    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session