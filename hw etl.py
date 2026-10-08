import mysql.connector
import csv
import os

# ============================================================
# 1. MYSQL CONNECTION
# ============================================================

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@ab0012",
        database="etlp"
    )

    cursor = con.cursor()

    print("Connected to MySQL")

except mysql.connector.Error as err:
    print("MySQL Connection Error:", err)
    exit()


# ============================================================
# 2. CREATE AMAZON TABLE
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Amazon")

create_table = """
CREATE TABLE Amazon (
    product_id VARCHAR(100),
    product_name TEXT,
    category TEXT,
    discounted_price DECIMAL(10,2),
    actual_price DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    rating DECIMAL(3,2),
    rating_count BIGINT,
    about_product TEXT,
    user_id TEXT,
    user_name TEXT,
    review_id TEXT,
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT
)
"""

cursor.execute(create_table)

print("Amazon table created")


# ============================================================
# 3. CSV FILE PATH
# ============================================================

# Keep amazon.csv in the same folder as this Python program

csv_file = "amazon.csv"

if not os.path.exists(csv_file):
    print("\nERROR: amazon.csv file not found!")
    print("Put amazon.csv in the same folder as hw etl.py")
    cursor.close()
    con.close()
    exit()


# ============================================================
# 4. READ CSV AND INSERT DATA
# ============================================================

print("\nReading CSV file...")

insert_query = """
INSERT INTO Amazon (
    product_id,
    product_name,
    category,
    discounted_price,
    actual_price,
    discount_percentage,
    rating,
    rating_count,
    about_product,
    user_id,
    user_name,
    review_id,
    review_title,
    review_content,
    img_link,
    product_link
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def clean_price(value):
    """Remove ₹ and commas from price."""
    if value is None or value.strip() == "":
        return None

    value = value.replace("₹", "").replace(",", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


def clean_percentage(value):
    """Remove % from discount percentage."""
    if value is None or value.strip() == "":
        return None

    value = value.replace("%", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


def clean_rating(value):
    """Convert rating into decimal."""
    if value is None or value.strip() == "":
        return None

    value = value.strip()

    try:
        return float(value)
    except ValueError:
        return None


def clean_rating_count(value):
    """Remove commas from rating count."""
    if value is None or value.strip() == "":
        return None

    value = value.replace(",", "").strip()

    try:
        return int(float(value))
    except ValueError:
        return None


count = 0

try:

    with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            data = (
                row.get("product_id"),
                row.get("product_name"),
                row.get("category"),

                clean_price(row.get("discounted_price")),
                clean_price(row.get("actual_price")),

                clean_percentage(row.get("discount_percentage")),
                clean_rating(row.get("rating")),
                clean_rating_count(row.get("rating_count")),

                row.get("about_product"),
                row.get("user_id"),
                row.get("user_name"),
                row.get("review_id"),
                row.get("review_title"),
                row.get("review_content"),
                row.get("img_link"),
                row.get("product_link")
            )

            cursor.execute(insert_query, data)

            count += 1

    con.commit()

    print("CSV data loaded successfully!")
    print("Records processed:", count)

except Exception as e:

    print("\nError while reading CSV:")
    print(e)

    con.rollback()

    cursor.close()
    con.close()

    exit()


# ============================================================
# 5. ETL OPERATION 1
# SELECT ALL DATA
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_All")

cursor.execute("""
CREATE TABLE Backup_All AS
SELECT *
FROM Amazon
""")

print("\n1. All data extracted")


# ============================================================
# 6. ETL OPERATION 2
# WHERE CONDITION
# Rating >= 4
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_High_Rating")

cursor.execute("""
CREATE TABLE Backup_High_Rating AS
SELECT *
FROM Amazon
WHERE rating >= 4
""")

print("2. Filtered data extracted")


# ============================================================
# 7. ETL OPERATION 3
# SELECT SPECIFIC COLUMNS
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Selected_Columns")

cursor.execute("""
CREATE TABLE Backup_Selected_Columns AS
SELECT
    product_id,
    product_name,
    category,
    rating,
    discounted_price
FROM Amazon
""")

print("3. Selected columns extracted")


# ============================================================
# 8. ETL OPERATION 4
# DISTINCT CATEGORY
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Categories")

cursor.execute("""
CREATE TABLE Backup_Categories AS
SELECT DISTINCT category
FROM Amazon
""")

print("4. Distinct categories extracted")


# ============================================================
# 9. ETL OPERATION 5
# ORDER BY RATING
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Rating_Sorted")

cursor.execute("""
CREATE TABLE Backup_Rating_Sorted AS
SELECT *
FROM Amazon
ORDER BY rating DESC
""")

print("5. Rating sorted data extracted")


# ============================================================
# 10. ETL OPERATION 6
# GROUP BY CATEGORY - COUNT
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Category_Count")

cursor.execute("""
CREATE TABLE Backup_Category_Count AS
SELECT
    category,
    COUNT(*) AS product_count
FROM Amazon
GROUP BY category
""")

print("6. Category count extracted")


# ============================================================
# 11. ETL OPERATION 7
# GROUP BY CATEGORY - AVERAGE RATING
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Average_Rating")

cursor.execute("""
CREATE TABLE Backup_Average_Rating AS
SELECT
    category,
    AVG(rating) AS average_rating
FROM Amazon
GROUP BY category
""")

print("7. Average rating extracted")


# ============================================================
# 12. ETL OPERATION 8
# HAVING
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_High_Average_Rating")

cursor.execute("""
CREATE TABLE Backup_High_Average_Rating AS
SELECT
    category,
    AVG(rating) AS average_rating
FROM Amazon
GROUP BY category
HAVING AVG(rating) >= 4
""")

print("8. HAVING result extracted")


# ============================================================
# 13. ETL OPERATION 9
# BETWEEN
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Price_Range")

cursor.execute("""
CREATE TABLE Backup_Price_Range AS
SELECT *
FROM Amazon
WHERE discounted_price BETWEEN 500 AND 5000
""")

print("9. BETWEEN result extracted")


# ============================================================
# 14. ETL OPERATION 10
# IN OPERATION
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Selected_Categories")

cursor.execute("""
CREATE TABLE Backup_Selected_Categories AS
SELECT *
FROM Amazon
WHERE category LIKE 'Computers&Accessories%'
   OR category LIKE 'Electronics%'
""")

print("10. Selected categories extracted")


# ============================================================
# 15. ETL OPERATION 11
# LIKE OPERATION
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Name_Search")

cursor.execute("""
CREATE TABLE Backup_Name_Search AS
SELECT *
FROM Amazon
WHERE product_name LIKE '%Cable%'
""")

print("11. LIKE result extracted")


# ============================================================
# 16. ETL OPERATION 12
# CASE OPERATION
# ============================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Rating_Category")

cursor.execute("""
CREATE TABLE Backup_Rating_Category AS
SELECT
    product_id,
    product_name,
    rating,

    CASE
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 4.0 THEN 'Good'
        WHEN rating >= 3.0 THEN 'Average'
        ELSE 'Poor'
    END AS rating_category

FROM Amazon
""")

print("12. CASE result extracted")


# ============================================================
# 17. COMMIT ALL CHANGES
# ============================================================

con.commit()

print("\n==========================================")
print("ETL COMPLETED SUCCESSFULLY!")
print("==========================================")


# ============================================================
# 18. SHOW RECORD COUNT
# ============================================================

cursor.execute("SELECT COUNT(*) FROM Amazon")

total_records = cursor.fetchone()[0]

print("Total records in Amazon table:", total_records)


# ============================================================
# 19. SHOW ALL TABLES
# ============================================================

print("\nTables created in ETL database:")

cursor.execute("SHOW TABLES")

for table in cursor.fetchall():
    print(table[0])


# ============================================================
# 20. CLOSE CONNECTION
# ============================================================

cursor.close()
con.close()

print("\nMySQL connection closed.")
print("Program finished successfully.")