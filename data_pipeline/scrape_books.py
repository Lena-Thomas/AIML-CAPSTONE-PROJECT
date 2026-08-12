"""
Module 1 - Step 2: Scraper
Scrapes raw book data from books.toscrape.com across multiple categories.
Saves the RAW (uncleaned) data to raw_books.csv.
No cleaning, no currency conversion, no database work happens here.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/"
MIN_BOOKS = 60          # official requirement: at least 60 books
MIN_CATEGORIES = 3      # official requirement: at least 3 categories
CATEGORIES_TO_SCRAPE = 5  # we scrape a few extra categories as a safety margin


def get_soup(url):
    """Download a page and turn it into a BeautifulSoup object we can search through."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # stops the script loudly if the page didn't load (e.g. 404)
    response.encoding = "utf-8"  # force correct text decoding (fixes Â£ / â garbling)
    return BeautifulSoup(response.text, "html.parser")


def get_category_links():
    """
    Visit the homepage and collect the links + names of every book category
    listed in the left-hand sidebar.
    """
    soup = get_soup(BASE_URL)
    sidebar_links = soup.select("div.side_categories ul li ul li a")

    categories = []
    for link in sidebar_links:
        name = link.get_text(strip=True)
        url = BASE_URL + link["href"]
        categories.append({"name": name, "url": url})

    return categories


def scrape_category(category_name, category_url):
    """
    Scrape every book on every page of a single category.
    Follows the "next" pagination link until there isn't one.
    Returns a list of dictionaries, one per book.
    """
    books = []
    current_url = category_url
    page_number = 1

    while current_url:
        print(f"  Scraping '{category_name}' page {page_number}...")
        soup = get_soup(current_url)

        book_cards = soup.select("article.product_pod")
        for card in book_cards:
            title = card.h3.a["title"]

            price_text = card.select_one("p.price_color").get_text(strip=True)

            # The star rating is stored as a CSS class, e.g. class="star-rating Three"
            rating_classes = card.select_one("p.star-rating")["class"]
            # rating_classes looks like ['star-rating', 'Three'] - we want the second word
            star_rating_text = [c for c in rating_classes if c != "star-rating"][0]

            availability_text = card.select_one("p.instock.availability").get_text(strip=True)

            books.append({
                "title": title,
                "price_gbp_raw": price_text,
                "star_rating_text": star_rating_text,
                "availability_text": availability_text,
                "category": category_name,
            })

        # Look for a "next" button to move to the next page of this category
        next_link = soup.select_one("li.next a")
        if next_link:
            # next_link href is relative to the current page's folder, so we
            # rebuild the full URL from the current page's address
            current_url = current_url.rsplit("/", 1)[0] + "/" + next_link["href"]
            page_number += 1
            time.sleep(0.3)  # small pause so we don't hammer the site with requests
        else:
            current_url = None  # no more pages in this category, stop the loop

    return books


def main():
    print("Fetching category list from books.toscrape.com...")
    all_categories = get_category_links()
    print(f"Found {len(all_categories)} categories on the site.\n")

    all_books = []
    categories_used = []

    for category in all_categories[:CATEGORIES_TO_SCRAPE]:
        print(f"Starting category: {category['name']}")
        category_books = scrape_category(category["name"], category["url"])
        all_books.extend(category_books)
        categories_used.append(category["name"])
        print(f"  -> {len(category_books)} books collected from '{category['name']}'\n")

        # Stop early once we've comfortably passed the minimum requirement
        if len(all_books) >= MIN_BOOKS and len(categories_used) >= MIN_CATEGORIES:
            print("Minimum requirement reached, stopping here.\n")
            break

    # Save the raw results
    df = pd.DataFrame(all_books)
    output_path = "data_pipeline/raw_books.csv"
    df.to_csv(output_path, index=False)

    # Final summary report
    print("=" * 50)
    print("SCRAPING COMPLETE")
    print("=" * 50)
    print(f"Total books scraped:      {len(df)}")
    print(f"Total categories scraped: {len(categories_used)}")
    print(f"Categories: {', '.join(categories_used)}")
    print(f"Saved to: {output_path}")

    if len(df) < MIN_BOOKS:
        print(f"\nWARNING: only {len(df)} books scraped, requirement is {MIN_BOOKS}.")
    if len(categories_used) < MIN_CATEGORIES:
        print(f"\nWARNING: only {len(categories_used)} categories scraped, requirement is {MIN_CATEGORIES}.")


if __name__ == "__main__":
    main()