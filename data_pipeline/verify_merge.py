"""
Module 1 - Step 9: pd.merge
Loads the raw 'books' and 'categories' tables into two separate DataFrames
(no JOIN in the SQL this time - just plain SELECT * for each table), then
reproduces Query 5's JOIN entirely in pandas using pd.merge.

Finally, compares this pandas-only result against sql_join_result.csv
(saved in Step 8) to prove the two approaches produce the same answer.
"""

import pandas as pd
import sqlite3

DB_PATH = "data_pipeline/books.db"
SQL_JOIN_RESULT_PATH = "data_pipeline/sql_join_result.csv"


def main():
    conn = sqlite3.connect(DB_PATH)

    # Load each table whole - no JOIN happens in SQL here, that's the point.
    print("Loading 'books' and 'categories' tables separately (no SQL JOIN)...")
    books_df = pd.read_sql("SELECT * FROM books", conn)
    categories_df = pd.read_sql("SELECT * FROM categories", conn)
    conn.close()

    print(f"books table: {books_df.shape}")
    print(f"categories table: {categories_df.shape}\n")

    # This is the actual pandas equivalent of the SQL JOIN:
    # match each book's category_id to the matching row in categories_df.
    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",   # the shared column both tables use to link rows
        how="inner"          # only keep books that have a matching category (same as SQL JOIN)
    )

    # Reproduce Query 5 exactly: same columns, same sort, same limit
    pandas_join_result = (
        merged_df[["title", "category_name", "price_inr"]]
        .sort_values("price_inr", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    print("pd.merge result (top 10 by price_inr):")
    print(pandas_join_result)
    print(f"Shape: {pandas_join_result.shape}\n")

    # Load the SQL JOIN result saved in Step 8 for comparison
    sql_join_result = pd.read_csv(SQL_JOIN_RESULT_PATH)

    print("SQL JOIN result (from Step 8, for comparison):")
    print(sql_join_result)
    print(f"Shape: {sql_join_result.shape}\n")

    # Compare the two results directly
    # Sort both the same way and reset index so row order can't cause a false mismatch
    sql_sorted = sql_join_result.sort_values("price_inr", ascending=False).reset_index(drop=True)
    pandas_sorted = pandas_join_result.sort_values("price_inr", ascending=False).reset_index(drop=True)

    results_match = sql_sorted.equals(pandas_sorted)

    print("=" * 50)
    print("COMPARISON RESULT")
    print("=" * 50)
    if results_match:
        print("MATCH: pd.merge produces the exact same result as the SQL JOIN.")
    else:
        print("MISMATCH: the two results are different - needs investigation.")
        print("\nDifferences:")
        print(pd.concat([sql_sorted, pandas_sorted]).drop_duplicates(keep=False))


if __name__ == "__main__":
    main()