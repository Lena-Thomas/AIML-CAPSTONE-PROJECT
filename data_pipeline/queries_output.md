# Module 1 - SQL Query Results


## Query 1 - The 5 cheapest in-stock books (by GBP price).
**Satisfies:** SELECT/WHERE, ORDER BY, LIMIT (M1.9)

```sql
SELECT title, price_gbp, in_stock
            FROM books
            WHERE in_stock = 1
            ORDER BY price_gbp ASC
            LIMIT 5
```

**Rows returned:** 5

| title | price_gbp | in_stock |
| --- | --- | --- |
| Tastes Like Fear (DI Marnie Rome #3) | 10.69 | 1 |
| Hide Away (Eve Duncan #20) | 11.84 | 1 |
| The Girl You Lost | 12.29 | 1 |
| Playing with Fire | 13.71 | 1 |
| That Darkness (Gardiner and Renner #1) | 13.92 | 1 |


## Query 2 - The distinct list of category names present in the database.
**Satisfies:** DISTINCT (M1.9)

```sql
SELECT DISTINCT category_name
            FROM categories
```

**Rows returned:** 3

| category_name |
| --- |
| Historical Fiction |
| Mystery |
| Travel |


## Query 3 - All books rated 4 or 5 stars (the 'highly rated' books).
**Satisfies:** IN (M1.9)

```sql
SELECT title, rating
            FROM books
            WHERE rating IN (4, 5)
```

**Rows returned:** 27

| title | rating |
| --- | --- |
| Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond | 4 |
| A Year in Provence (Provence #1) | 4 |
| 1,000 Places to See Before You Die | 5 |
| Sharp Objects | 4 |
| The Past Never Ends | 4 |
| The Murder of Roger Ackroyd (Hercule Poirot #4) | 4 |
| A Time of Torment (Charlie Parker #14) | 5 |
| Murder at the 42nd Street Library (Raymond Ambler #1) | 4 |
| What Happened on Beale Street (Secrets of the South Mysteries #2) | 5 |
| The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) | 5 |
| Delivering the Truth (Quaker Midwife Mystery #1) | 4 |
| The Mysterious Affair at Styles (Hercule Poirot #1) | 4 |
| The Silkworm (Cormoran Strike #2) | 5 |
| The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1) | 4 |
| The Girl You Lost | 5 |
| A Flight of Arrows (The Pathfinders #2) | 5 |
| Mrs. Houdini | 5 |
| The Marriage of Opposites | 4 |
| A Paris Apartment | 4 |
| World Without End (The Pillars of the Earth #2) | 4 |
| The Passion of Dolssa | 5 |
| Voyager (Outlander #3) | 5 |
| The Red Tent | 5 |
| Between Shades of Gray | 5 |
| While You Were Mine | 5 |
| Lost Among the Living | 4 |
| A Spy's Devotion (The Regency Spies of London #1) | 5 |


## Query 4 - Books priced between £20 and £40 (a 'mid-range price' filter).
**Satisfies:** BETWEEN (M1.9)

```sql
SELECT title, price_gbp
            FROM books
            WHERE price_gbp BETWEEN 20 AND 40
```

**Rows returned:** 33

| title | price_gbp |
| --- | --- |
| Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel | 36.94 |
| Under the Tuscan Sun | 37.33 |
| The Great Railway Bazaar | 30.54 |
| The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2) | 23.21 |
| Neither Here nor There: Travels in Europe | 38.95 |
| 1,000 Places to See Before You Die | 26.08 |
| Poisonous (Max Revere Novels #3) | 26.8 |
| Most Wanted | 35.28 |
| The Widow | 27.26 |
| What Happened on Beale Street (Secrets of the South Mysteries #2) | 25.37 |
| Delivering the Truth (Quaker Midwife Mystery #1) | 20.89 |
| The Mysterious Affair at Styles (Hercule Poirot #1) | 24.8 |
| In the Woods (Dublin Murder Squad #1) | 38.38 |
| The Silkworm (Cormoran Strike #2) | 23.05 |
| Extreme Prey (Lucas Davenport #26) | 25.4 |
| Career of Evil (Cormoran Strike #3) | 24.72 |
| Blood Defense (Samantha Brinkman #1) | 20.3 |
| Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton | 29.69 |
| The House by the Lake | 36.95 |
| Mrs. Houdini | 30.25 |
| The Marriage of Opposites | 28.08 |
| Love, Lies and Spies | 20.55 |
| A Paris Apartment | 39.01 |
| The Invention of Wings | 37.34 |
| World Without End (The Pillars of the Earth #2) | 32.97 |
| The Passion of Dolssa | 28.32 |
| Girl With a Pearl Earring | 26.77 |
| Voyager (Outlander #3) | 21.07 |
| The Red Tent | 35.66 |
| Between Shades of Gray | 20.79 |
| The Secret Healer | 34.56 |
| Starlark | 25.83 |
| Lost Among the Living | 27.7 |


## Query 5 - Every book shown together with its category name, by joining the books and categories tables.
**Satisfies:** JOIN (M1.9)

```sql
SELECT books.title, categories.category_name, books.price_inr
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            ORDER BY books.price_inr DESC
            LIMIT 10
```

**Rows returned:** 10

| title | category_name | price_inr |
| --- | --- | --- |
| Boar Island (Anna Pigeon #19) | Mystery | 6275.14 |
| The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1) | Mystery | 6087.35 |
| A Year in Provence (Provence #1) | Travel | 6000.84 |
| The Past Never Ends | Mystery | 5960.75 |
| The Last Painting of Sara de Vos | Historical Fiction | 5860.52 |
| A Flight of Arrows (The Pathfinders #2) | Historical Fiction | 5858.42 |
| Murder at the 42nd Street Library (Raymond Ambler #1) | Mystery | 5734.98 |
| The Last Mile (Amos Decker #2) | Mystery | 5719.16 |
| 1st to Die (Women's Murder Club #1) | Mystery | 5694.89 |
| Tipping the Velvet | Historical Fiction | 5669.57 |


## Query 6 - How many books fall into each category.
**Satisfies:** GROUP BY + COUNT (additional, beyond M1.9 minimum)

```sql
SELECT categories.category_name, COUNT(books.book_id) AS book_count
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            GROUP BY categories.category_name
            ORDER BY book_count DESC
```

**Rows returned:** 3

| category_name | book_count |
| --- | --- |
| Mystery | 32 |
| Historical Fiction | 26 |
| Travel | 11 |


## Query 7 - The average GBP price of books within each category.
**Satisfies:** GROUP BY + AVG (additional, beyond M1.9 minimum)

```sql
SELECT categories.category_name, ROUND(AVG(books.price_gbp), 2) AS avg_price_gbp
            FROM books
            JOIN categories ON books.category_id = categories.category_id
            GROUP BY categories.category_name
            ORDER BY avg_price_gbp DESC
```

**Rows returned:** 3

| category_name | avg_price_gbp |
| --- | --- |
| Travel | 39.79 |
| Historical Fiction | 33.64 |
| Mystery | 31.72 |
