"""Product scraper: collects title, price, rating and availability from a
catalog site with pagination and saves the result to CSV or JSON.

Demo target: https://books.toscrape.com (a sandbox site made for scraping practice).

Usage:
    python scraper.py --pages 3 --out books.csv
    python scraper.py --pages 0 --out books.json   # 0 = all pages
"""

import argparse
import csv
import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio scraper demo)"}


def fetch(session: requests.Session, url: str, retries: int = 3) -> str:
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as e:
            if attempt == retries:
                raise
            wait = 2**attempt
            print(f"  ! {e} — retrying in {wait}s")
            time.sleep(wait)
    raise AssertionError("unreachable")


def parse_page(html: str, page_url: str) -> tuple[list[dict], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        rating_class = card.select_one("p.star-rating")["class"]
        items.append(
            {
                "title": link["title"],
                "price": float(card.select_one("p.price_color").text.lstrip("£Â")),
                "currency": "GBP",
                "rating": next((RATINGS[c] for c in rating_class if c in RATINGS), None),
                "in_stock": "In stock" in card.select_one("p.availability").text,
                "url": urljoin(page_url, link["href"]),
            }
        )
    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return items, next_url


def scrape(max_pages: int, delay: float) -> list[dict]:
    results: list[dict] = []
    url: str | None = START_URL
    page = 0
    with requests.Session() as session:
        while url and (max_pages == 0 or page < max_pages):
            page += 1
            print(f"Page {page}: {url}")
            items, url = parse_page(fetch(session, url), url)
            results.extend(items)
            if url:
                time.sleep(delay)  # be polite to the server
    return results


def save(rows: list[dict], path: str) -> None:
    if path.endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
    else:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pages", type=int, default=2, help="pages to scrape, 0 = all")
    parser.add_argument("--out", default="books.csv", help="output file (.csv or .json)")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    args = parser.parse_args()

    rows = scrape(args.pages, args.delay)
    if not rows:
        print("Nothing scraped.")
        return
    save(rows, args.out)
    avg = sum(r["price"] for r in rows) / len(rows)
    print(f"Saved {len(rows)} items to {args.out} (average price £{avg:.2f})")


if __name__ == "__main__":
    main()
