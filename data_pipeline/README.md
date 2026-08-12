# Module 1 — Data Pipeline

This module scrapes book data from [books.toscrape.com](https://books.toscrape.com), cleans it, converts prices to INR, loads it into a normalized SQLite database, and demonstrates equivalent SQL and pandas approaches to querying it.

## Installation

From the project root, with your virtual environment activated:

```
pip install -r data_pipeline/requirements.txt
```

This installs the 3 packages this module needs: `requests`, `beautifulsoup4`, `pandas`. (`sqlite3` is part of Python's standard library — no install needed.)

## How to run (in order)

Each script produces a file the next script depends on, so run them in this exact order:

| Step | Command | Produces |
|---|---|---|
| 1 | `python data_pipeline\scrape_books.py` | `raw_books.csv` |
| 2 | `python data_pipeline\verify_raw_data.py` | (verification only) |
| 3 | `python data_pipeline\clean_books.py` | `clean_books.csv` |
| 4 | `python data_pipeline\convert_currency.py` | adds `price_inr` to `clean_books.csv` |
| 5 | `python data_pipeline\build_database.py` | `books.db` |
| 6 | `python data_pipeline\run_queries.py` | `queries_output.md` |
| 7 | `python data_pipeline\read_with_pandas.py` | `sql_join_result.csv` |
| 8 | `python data_pipeline\verify_merge.py` | (comparison only) |

`books.db` can be fully regenerated from scratch at any time by re-running steps 1–5 in order.

## Data source

Books were scraped live from `books.toscrape.com`, a public site built specifically for scraping practice. 69 books were collected across 3 categories: **Travel, Mystery, Historical Fiction** — exceeding the required minimums of 60 books / 3 categories.

## Key design decisions

**Encoding fix:** the site's pages needed `response.encoding = "utf-8"` set explicitly on each `requests` call. Without it, special characters (apostrophes, accented letters) were garbled (e.g. `Â£` instead of `£`). This is set in `scrape_books.py`'s `get_soup()` function.

**Handling unparsable rows (M1.5):** if a book's price or rating cannot be parsed into a valid number, that row is **dropped**, not guessed at, and a warning is printed naming the exact row. This was chosen over imputing a fake value because an unparsable price/rating usually signals a malformed row (e.g. missing data on the source page) rather than a genuinely missing statistic that could be reasonably estimated. In this run, 0 rows required dropping — every scraped row parsed cleanly.

**Currency conversion (M1.6):** `price_inr` is calculated using the **fixed, mandatory rate of 1 GBP = 105.50 INR**, applied as `price_gbp × 105.50`. This is a fixed constant in `convert_currency.py`, not a live exchange-rate lookup, per the official requirement. (Minor note: at exact half-paisa boundaries, e.g. `49.43 × 105.50 = 5214.865`, Python's rounding gives `5214.86` rather than `5214.87` due to standard "round-half-to-even" floating-point behavior — a harmless, well-known property of how computers round numbers, not an error in the rate itself.)

**Database schema (M1.7):** normalized into two tables — `categories` (category_id, category_name) and `books` (book_id, title, price_gbp, price_inr, rating, in_stock, category_id) — linked by a primary key / foreign key relationship on `category_id`. This avoids repeating category text on every book row.

## SQL queries (M1.9)

7 queries were run against the database. The first 5 satisfy the mandatory M1.9 requirement, together covering every required clause type: `SELECT/WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `IN`, `BETWEEN`, and `JOIN`. Two additional queries (6–7) were added afterward to demonstrate `GROUP BY` aggregation — books per category (`COUNT`) and average price per category (`AVG`) — beyond the minimum requirement. Full query text and results for all 7 are saved in `queries_output.md`.

## pandas verification (M1.10, M1.11)

Two query results were loaded via `pd.read_sql`. The JOIN query was independently reproduced using `pd.merge` on the raw `books` and `categories` tables (no SQL JOIN involved), and verified to produce an identical result to the SQL JOIN — confirming the two approaches are equivalent.

## Files in this module

| File | Purpose |
|---|---|
| `requirements.txt` | pip dependencies |
| `scrape_books.py` | scrapes raw book data |
| `raw_books.csv` | raw scraped output |
| `verify_raw_data.py` | checks raw data against acceptance criteria |
| `clean_books.py` | cleans price/rating/availability fields |
| `clean_books.csv` | cleaned data (later gains `price_inr`) |
| `convert_currency.py` | adds `price_inr` using the fixed rate |
| `build_database.py` | builds the normalized SQLite database |
| `books.db` | the SQLite database |
| `run_queries.py` | runs the 7 SQL queries (5 required + 2 additional) |
| `queries_output.md` | full SQL query results |
| `read_with_pandas.py` | loads 2 query results via `pd.read_sql` |
| `sql_join_result.csv` | JOIN result, saved for comparison |
| `verify_merge.py` | reproduces JOIN via `pd.merge`, compares to SQL result |
| `README.md` | this file |