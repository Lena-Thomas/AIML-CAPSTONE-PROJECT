"""
Module 1 - Step 8: pd.read_sql
Reads 2 of the SQL queries from Step 7 directly into pandas DataFrames using
pd.read_sql, instead of the plain sqlite3 cursor we used before.

We deliberately reuse:
  - the JOIN query (Query 5 from Step 7) - because Step 9 will need this
    exact result as a DataFrame to compare against pd.merge
  - the WHERE/ORDER BY/LIMIT query (Query 1 from Step 7) - to show
    pd.read_sql works the same way for a non-JOIN query too

Does NOT do pd.merge yet (that is Step 9).
"""

import pandas as pd
import sqlite3

DB_PATH = "data_pipeline/books.db"

QUERY_1_SQL = """
    SELECT title, price_gbp, in_stock
    FROM books
    WHERE in_stock = 1
    ORDER BY price_gbp ASC
    LIMIT 5
"""

QUERY_5_JOIN_SQL = """
    SELECT books.title, categories.category_name, books.price_inr
    FROM books
    JOIN categories ON books.category_id = categories.category_id
    ORDER BY books.price_inr DESC
    LIMIT 10
"""


def main():
    conn = sqlite3.connect(DB_PATH)

    print("Reading Query 1 (cheapest in-stock books) via pd.read_sql...")
    df_query1 = pd.read_sql(QUERY_1_SQL, conn)
    print(df_query1)
    print(f"Shape: {df_query1.shape}\n")

    print("Reading Query 5 (JOIN - books with category names) via pd.read_sql...")
    df_query5_join = pd.read_sql(QUERY_5_JOIN_SQL, conn)
    print(df_query5_join)
    print(f"Shape: {df_query5_join.shape}\n")

    conn.close()

    # Save the JOIN result to disk so Step 9 can load it and compare
    # against a pandas-only pd.merge, without needing to touch the database again.
    df_query5_join.to_csv("data_pipeline/sql_join_result.csv", index=False)

    print("=" * 50)
    print("PD.READ_SQL COMPLETE")
    print("=" * 50)
    print(f"Query 1 DataFrame shape: {df_query1.shape}")
    print(f"Query 5 (JOIN) DataFrame shape: {df_query5_join.shape}")
    print("Saved JOIN result to: data_pipeline/sql_join_result.csv (used by Step 9)")


if __name__ == "__main__":
    main()