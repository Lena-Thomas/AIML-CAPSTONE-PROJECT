"""
Module 1 - Step 4: Cleaning
Reads raw_books.csv and converts the raw text fields into proper typed columns:
  price_gbp_raw   (text like "£45.17")   -> price_gbp   (float)
  star_rating_text (word like "Three")   -> rating       (int 1-5)
  availability_text (sentence)           -> in_stock     (bool)

Design decision (per official requirement M1.5 - handling parse failures):
If a row's price or rating cannot be parsed, we DROP that row rather than
guessing a value, and we print a warning naming the row so nothing is lost
silently. We chose "drop" over "impute" because a book with an unparseable
price/rating is a sign the row itself is malformed (not just missing data),
so imputing a fake number would misrepresent that specific book rather than
fill in a genuinely missing statistic.

Does NOT do currency conversion (that is Step 5) and does NOT touch the database.
"""

import pandas as pd
import re

INPUT_PATH = "data_pipeline/raw_books.csv"
OUTPUT_PATH = "data_pipeline/clean_books.csv"

RATING_WORD_TO_INT = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_price(raw_price):
    """
    Turn '£45.17' into 45.17 (a float).
    Returns None if the text doesn't contain a valid number, so the caller
    can decide to drop that row.
    """
    match = re.search(r"[\d]+\.[\d]+", str(raw_price))
    if match:
        return float(match.group())
    return None


def parse_rating(raw_rating):
    """
    Turn 'Three' into 3 (an int) using the lookup table above.
    Returns None if the word isn't one of the five expected ratings.
    """
    return RATING_WORD_TO_INT.get(str(raw_rating).strip(), None)


def parse_availability(raw_availability):
    """
    Turn 'In stock (19 available)' or 'In stock' into True.
    Turn anything mentioning 'out of stock' into False.
    """
    text = str(raw_availability).lower()
    return "in stock" in text


def main():
    print("Loading raw data...")
    df = pd.read_csv(INPUT_PATH)
    starting_rows = len(df)
    print(f"Loaded {starting_rows} raw rows.\n")

    # Apply each parser to build the new clean columns
    df["price_gbp"] = df["price_gbp_raw"].apply(parse_price)
    df["rating"] = df["star_rating_text"].apply(parse_rating)
    df["in_stock"] = df["availability_text"].apply(parse_availability)

    # Find rows where price or rating failed to parse (rating/price is None)
    failed_mask = df["price_gbp"].isnull() | df["rating"].isnull()
    failed_rows = df[failed_mask]

    if len(failed_rows) > 0:
        print(f"WARNING: {len(failed_rows)} row(s) could not be parsed and will be DROPPED:")
        for idx, row in failed_rows.iterrows():
            print(f"  - Row {idx}: title='{row['title']}', "
                  f"price_raw='{row['price_gbp_raw']}', rating_raw='{row['star_rating_text']}'")
    else:
        print("No parsing failures found - every row converted cleanly.\n")

    # Drop the failed rows (our documented policy - see module docstring)
    df_clean = df[~failed_mask].copy()

    # Keep only the columns we need going forward, in a clean order
    df_clean = df_clean[["title", "price_gbp", "rating", "in_stock", "category"]]

    # Ensure correct dtypes explicitly (rating as whole numbers, not floats)
    df_clean["rating"] = df_clean["rating"].astype(int)
    df_clean["in_stock"] = df_clean["in_stock"].astype(bool)

    df_clean.to_csv(OUTPUT_PATH, index=False)

    print("\n" + "=" * 50)
    print("CLEANING COMPLETE")
    print("=" * 50)
    print(f"Rows before cleaning: {starting_rows}")
    print(f"Rows dropped (parse failures): {len(failed_rows)}")
    print(f"Rows after cleaning:  {len(df_clean)}")
    print(f"Columns: {list(df_clean.columns)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()