"""
Module 1 - Step 7: SQL Queries
Runs 7 SQL queries against books.db using plain sqlite3 (no pandas -
pd.read_sql is handled separately in read_with_pandas.py).

Queries 1-5 are the original required set, covering every required clause:
  Query 1 - SELECT/WHERE, ORDER BY, LIMIT
  Query 2 - DISTINCT
  Query 3 - IN
  Query 4 - BETWEEN
  Query 5 - JOIN (categories + books)

Queries 6-7 are additional queries demonstrating GROUP BY aggregation,
added after the mandatory M1.9 requirement was already satisfied:
  Query 6 - GROUP BY + COUNT (books per category)
  Query 7 - GROUP BY + AVG (average price per category)

Results are printed to the terminal AND saved to queries_output.md so there
is a permanent record of the query text and its results.
"""

import sqlite3

DB_PATH = "data_pipeline/books.db"
OUTPUT_PATH = "data_pipeline/queries_output.md"

QUERIES = [
    {
        "id": "Query 1",
        "satisfies": "SELECT/WHERE, ORDER BY, LIMIT (M1.9)",
        "description": "The 5 cheapest in-stock books (by GBP price).",
        "sql": """
            SELECT title, price_gbp, in_stock
            FROM books
            WHERE in_stock = 1
            ORDER BY price_gbp ASC
            LIMIT 5
        """,
    },
    {
        "id": "Query 2",
        "satisfies": "DISTINCT (M1.9)",
        "description": "The distinct list of category names present in the database.",
        "sql": """
            SELECT DISTINCT category_name
            FROM categories
        """,
    },
    {
        "id": "Query 3",
        "satisfies": "IN (M1.9)",
        "description": "All books rated 4 or 5 stars (the 'highly rated' books).",
        "sql": """
            SELECT title, rating
            FROM books
            WHERE rating IN (4, 5)
        """,
    },
    {
        "id": "Query 4",
        "satisfies": "BETWEEN (M1.9)",
        "description": "Books priced between £20 and £40 (a 'mid-range price' filter).",
        "sql": """
            SELECT title, price_gbp
            FROM books
            WHERE price_gbp BETWEEN 20 AND 40
        """,
    },
    {
        "id": "Query 5",
        "satisfies": "JOIN (M1.9)",
        "description": "Every book shown together with its category name, "
                        "by joining the books and categories tables.",
        "sql": """
            SELECT books.title, categories.category_name, books.price_inr
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            ORDER BY books.price_inr DESC
            LIMIT 10
        """,
    },
    {
        "id": "Query 6",
        "satisfies": "GROUP BY + COUNT (additional, beyond M1.9 minimum)",
        "description": "How many books fall into each category.",
        "sql": """
            SELECT categories.category_name, COUNT(books.book_id) AS book_count
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            GROUP BY categories.category_name
            ORDER BY book_count DESC
        """,
    },
    {
        "id": "Query 7",
        "satisfies": "GROUP BY + AVG (additional, beyond M1.9 minimum)",
        "description": "The average GBP price of books within each category.",
        "sql": """
            SELECT categories.category_name, ROUND(AVG(books.price_gbp), 2) AS avg_price_gbp
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            GROUP BY categories.category_name
            ORDER BY avg_price_gbp DESC
        """,
    },
]


def run_query(cursor, sql):
    cursor.execute(sql)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    return columns, rows


def format_as_markdown_table(columns, rows):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body_lines = []
    for row in rows:
        body_lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join([header, separator] + body_lines)


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    output_sections = ["# Module 1 - SQL Query Results\n"]

    for query in QUERIES:
        print("=" * 60)
        print(f"{query['id']}: {query['description']}")
        print(f"Satisfies: {query['satisfies']}")
        print("-" * 60)

        columns, rows = run_query(cursor, query["sql"])

        print(f"Columns: {columns}")
        print(f"Rows returned: {len(rows)}")
        for row in rows[:5]:  # only show first 5 in the terminal to keep it readable
            print(f"  {row}")
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more (full results saved to {OUTPUT_PATH})")
        print()

        # Build the markdown section for this query
        section = f"## {query['id']} - {query['description']}\n"
        section += f"**Satisfies:** {query['satisfies']}\n\n"
        section += f"```sql\n{query['sql'].strip()}\n```\n\n"
        section += f"**Rows returned:** {len(rows)}\n\n"
        section += format_as_markdown_table(columns, rows) + "\n"
        output_sections.append(section)

    conn.close()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(output_sections))

    print("=" * 60)
    print("ALL QUERIES COMPLETE")
    print(f"Full results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()