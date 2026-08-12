"""
Module 1 - Step 6: Build the SQLite database
Reads clean_books.csv and loads it into a normalized SQLite database with
two tables linked by a primary/foreign key relationship:

    categories (category_id PK, category_name)
    books      (book_id PK, title, price_gbp, price_inr, rating, in_stock,
                 category_id FK -> categories.category_id)

This is "normalized" because the category name is stored once in the
categories table, and books simply reference it by ID - avoiding repeating
the same category text on every single book row.

Does NOT run any SQL queries yet (that is Step 7).
"""

import pandas as pd
import sqlite3
import os

CSV_PATH = "data_pipeline/clean_books.csv"
DB_PATH = "data_pipeline/books.db"


def main():
    print("Loading cleaned data...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} rows.\n")

    # Start fresh each time this script runs, so re-running it never
    # duplicates data or leaves an old schema lying around.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing books.db so we can rebuild it cleanly.\n")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Create the categories table ---
    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    """)

    # --- Create the books table, with a foreign key pointing at categories ---
    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL NOT NULL,
            price_inr REAL NOT NULL,
            rating INTEGER NOT NULL,
            in_stock INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    """)
    print("Created tables: categories, books\n")

    # --- Insert each unique category once ---
    unique_categories = sorted(df["category"].unique())
    for category_name in unique_categories:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category_name,)
        )
    print(f"Inserted {len(unique_categories)} categories: {unique_categories}\n")

    # Build a lookup so we know which category_id belongs to each category name
    cursor.execute("SELECT category_id, category_name FROM categories")
    category_lookup = {name: cid for cid, name in cursor.fetchall()}

    # --- Insert each book, linked to its category's ID ---
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            int(row["rating"]),
            int(row["in_stock"]),  # SQLite stores booleans as 0/1
            category_lookup[row["category"]],
        ))

    conn.commit()

    # --- Report back row counts straight from the database, as proof ---
    cursor.execute("SELECT COUNT(*) FROM books")
    books_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM categories")
    categories_count = cursor.fetchone()[0]

    conn.close()

    print("=" * 50)
    print("DATABASE BUILD COMPLETE")
    print("=" * 50)
    print(f"Database file: {DB_PATH}")
    print(f"categories table rows: {categories_count}")
    print(f"books table rows: {books_count}")


if __name__ == "__main__":
    main()