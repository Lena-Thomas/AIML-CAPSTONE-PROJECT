"""
Module 1 - Step 5: Currency Conversion
Reads clean_books.csv and adds a price_inr column using the MANDATORY fixed rate:

    1 GBP = 105.50 INR

This fixed rate is an official requirement - it is NOT looked up from a live
API. No optional live-currency-API feature is implemented at this stage
(that is explicitly out of scope until every mandatory requirement is done).

Overwrites clean_books.csv in place, adding the new column, so there is
still a single source of truth going into the database step.
"""

import pandas as pd

DATA_PATH = "data_pipeline/clean_books.csv"

GBP_TO_INR_RATE = 105.50  # official fixed rate - do not replace with a live lookup


def main():
    print("Loading cleaned data...")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} rows.\n")

    if "price_inr" in df.columns:
        print("price_inr column already exists - it will be recalculated.\n")

    # The actual conversion: multiply every price_gbp value by the fixed rate
    df["price_inr"] = (df["price_gbp"] * GBP_TO_INR_RATE).round(2)

    df.to_csv(DATA_PATH, index=False)

    print("=" * 50)
    print("CURRENCY CONVERSION COMPLETE")
    print("=" * 50)
    print(f"Rate used: 1 GBP = {GBP_TO_INR_RATE} INR")
    print(f"Rows converted: {len(df)}")
    print(f"Columns now: {list(df.columns)}")
    print("\nSample check (first 5 rows):")
    print(df[["title", "price_gbp", "price_inr"]].head(5).to_string(index=False))
    print(f"\nSaved to: {DATA_PATH}")


if __name__ == "__main__":
    main()