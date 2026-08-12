"""
Module 1 - Step 3: Verify raw scraped data
Checks raw_books.csv against the official acceptance criteria.
Does NOT clean anything - this only reports problems.
"""

import pandas as pd
import os

CSV_PATH = "data_pipeline/raw_books.csv"
MIN_BOOKS = 60
MIN_CATEGORIES = 3
REQUIRED_COLUMNS = ["title", "price_gbp_raw", "star_rating_text", "availability_text", "category"]
VALID_RATING_WORDS = {"One", "Two", "Three", "Four", "Five"}


def check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {label}" + (f" - {detail}" if detail else ""))
    return passed


def main():
    print("=" * 50)
    print("VERIFYING raw_books.csv")
    print("=" * 50)

    all_passed = True

    # 1. File exists
    exists = os.path.exists(CSV_PATH)
    all_passed &= check("File exists", exists, CSV_PATH)
    if not exists:
        print("\nStopping - cannot check further without the file.")
        return

    df = pd.read_csv(CSV_PATH)

    # 2. Row count
    all_passed &= check("At least 60 rows", len(df) >= MIN_BOOKS, f"found {len(df)} rows")

    # 3. Category count
    num_categories = df["category"].nunique()
    all_passed &= check("At least 3 categories", num_categories >= MIN_CATEGORIES,
                         f"found {num_categories}: {list(df['category'].unique())}")

    # 4. Required columns present
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    all_passed &= check("All 5 required columns present", len(missing_cols) == 0,
                         f"missing: {missing_cols}" if missing_cols else "all present")

    # 5a. Price still raw (should contain a currency symbol/text, not be a plain float)
    price_looks_raw = df["price_gbp_raw"].astype(str).str.contains(r"£|Â£", regex=True).all()
    all_passed &= check("Price column still RAW (has currency symbol)", price_looks_raw)

    # 5b. Rating still words, not numbers
    ratings_are_words = df["star_rating_text"].isin(VALID_RATING_WORDS).all()
    all_passed &= check("Rating column still RAW (words like 'Three')", ratings_are_words)

    # 5c. Availability still full text, not boolean
    availability_is_text = df["availability_text"].astype(str).str.contains("stock", case=False).all()
    all_passed &= check("Availability column still RAW (text, not boolean)", availability_is_text)

    # 6. No completely empty required fields
    has_nulls = df[REQUIRED_COLUMNS].isnull().any().any()
    all_passed &= check("No missing/blank values in required columns", not has_nulls)

    # 6b. Encoding check - flag garbled characters
    encoding_issue = df["price_gbp_raw"].astype(str).str.contains("Â").any() or \
                      df["title"].astype(str).str.contains("â|Â").any()
    check("No encoding corruption (Â/â artifacts)", not encoding_issue,
          "GARBLED TEXT DETECTED - see fix instructions" if encoding_issue else "")
    # Note: encoding issue does NOT flip all_passed to False on its own here -
    # we report it separately below with a clear fix, since it's fixable by re-scraping.

    print("\n" + "=" * 50)
    if all_passed and not encoding_issue:
        print("RESULT: All checks passed. Step 2 scraping is ACCEPTED.")
    elif all_passed and encoding_issue:
        print("RESULT: Structural checks passed, BUT encoding is corrupted.")
        print("Fix required before moving to Step 4 (cleaning). See instructions.")
    else:
        print("RESULT: One or more checks FAILED. Do not proceed to Step 4 yet.")
    print("=" * 50)


if __name__ == "__main__":
    main()