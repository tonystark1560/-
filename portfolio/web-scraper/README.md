# Product Catalog Scraper

A Python scraper that walks through a paginated product catalog and exports
title, price, rating, stock status and link to **CSV or JSON**.

Demo target: [books.toscrape.com](https://books.toscrape.com), a sandbox site built
for scraping practice. The same structure can be adapted to e-commerce sites,
directories and listing sites.

## Features

- Follows pagination automatically (`--pages 0` = all pages)
- Exports to CSV (opens in Excel / Google Sheets) or JSON
- Retries with exponential backoff on network errors
- Delay between requests so the target server isn't overloaded
- Clean, typed data: prices as numbers, rating as 1–5, stock as true/false

## Usage

```bash
cd portfolio/web-scraper
pip install -r requirements.txt
python scraper.py --pages 3 --out books.csv
python scraper.py --pages 0 --out books.json
```

Example output: [`sample_output.csv`](sample_output.csv)

```
Page 1: https://books.toscrape.com/catalogue/page-1.html
Page 2: https://books.toscrape.com/catalogue/page-2.html
Saved 40 items to books.csv (average price £34.96)
```

## Tech stack

Python 3.11+ · requests · BeautifulSoup4
