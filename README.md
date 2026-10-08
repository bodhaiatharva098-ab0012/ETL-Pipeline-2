# Amazon Product ETL Pipeline with Python & MySQL

A beginner-friendly ETL workflow that uses **Python, CSV, and MySQL** to extract Amazon product data, clean and transform it with Python and SQL, and load the results into separate analysis and backup tables.

## Overview

The pipeline reads Amazon product data from a CSV file, connects to a MySQL database using `mysql-connector-python`, creates an `Amazon` table, cleans the product data, and runs SQL operations to create **12 derived tables**. The project demonstrates filtering, selecting, sorting, grouping, aggregation, searching, and categorizing data.

### ETL workflow

1. **Extract** Amazon product records from the `amazon.csv` file.
2. **Transform** the data using Python to clean prices, discounts, ratings, and rating counts.
3. **Load** the cleaned data into the MySQL `Amazon` table.
4. **Transform and analyze** the data using SQL operations such as `WHERE`, `DISTINCT`, `ORDER BY`, `GROUP BY`, aggregates, `HAVING`, `BETWEEN`, `LIKE`, and `CASE`.
5. **Load** each SQL result into its own MySQL backup/analysis table.

## Tables created

| Table                        | Example operation                                           |
| ---------------------------- | ----------------------------------------------------------- |
| `Backup_All`                 | Copy all Amazon product rows                                |
| `Backup_High_Rating`         | Filter products with rating 4 or higher                     |
| `Backup_Selected_Columns`    | Keep selected product columns                               |
| `Backup_Categories`          | Select distinct product categories                          |
| `Backup_Rating_Sorted`       | Sort products by rating descending                          |
| `Backup_Category_Count`      | Count products by category                                  |
| `Backup_Average_Rating`      | Calculate average rating by category                        |
| `Backup_High_Average_Rating` | Keep categories with average rating 4 or higher             |
| `Backup_Price_Range`         | Filter prices between ₹500 and ₹5,000                       |
| `Backup_Selected_Categories` | Select products from Computers & Accessories or Electronics |
| `Backup_Name_Search`         | Find product names containing `Cable`                       |
| `Backup_Rating_Category`     | Assign rating categories using `CASE`                       |

> The rating, price, category, and product-name filters can be changed according to your requirements.

## Screenshots

### ETL workflow

![Amazon Python and MySQL ETL workflow](https://github.com/bodhaiatharva098-ab0012/ETL-Pipeline-2/blob/main/Etl%20pipeline%202.jpg)

### MySQL Workbench results

![MySQL Workbench showing the Amazon database tables and results](https://github.com/bodhaiatharva098-ab0012/ETL-Pipeline-2/blob/main/Screenshot%202026-10-08%20115037.jpg)
![MySQL Workbench showing the Amazon database tables and results](https://github.com/bodhaiatharva098-ab0012/ETL-Pipeline-2/blob/main/Screenshot%202026-10-08%20115020.jpg)
![MySQL Workbench showing the Amazon database tables and results](https://github.com/bodhaiatharva098-ab0012/ETL-Pipeline-2/blob/main/Screenshot%202026-10-08%20115004.jpg)
Add the screenshots to the repository at `workflow.png` and `assets/mysql-workbench.png`. The workflow image should show the **CSV → Python ETL → MySQL → SQL Analysis** process, while the Workbench screenshot should show the created database tables or query results.

## Requirements

* Python 3
* MySQL Server
* MySQL Workbench (optional, for browsing tables and query results)
* Amazon product CSV dataset
* Python packages:

  * `mysql-connector-python`

Install the MySQL connector:

```bash
python -m pip install mysql-connector-python
```

## Configure the database connection

Create the target database in MySQL and configure the connection in the Python script.

For security, avoid committing your MySQL password to GitHub. One option is to use environment variables:

```python
import os
import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "etl"),
)
```

Set `MYSQL_USER` and `MYSQL_PASSWORD` in your local environment before running the script.

Make sure the configured MySQL database exists and the account has permission to create and insert data into tables.

## Run

1. Start MySQL Server.
2. Create the target database.
3. Place `amazon.csv` in the same folder as the Python ETL program.
4. Install the Python dependency:

```bash
python -m pip install mysql-connector-python
```

5. Configure your MySQL connection.
6. Run the ETL script from the repository folder:

```bash
python etl_pipeline.py
```

7. Refresh the schema in MySQL Workbench.
8. Check the `Amazon` table and the generated `Backup_*` tables.

If your Python file has a different name, replace `etl_pipeline.py` with your actual filename.

## Data Cleaning

The Python ETL process performs several data-cleaning operations before inserting the records into MySQL:

* Removes `₹` symbols from prices.
* Removes commas from numeric values.
* Removes `%` from discount percentages.
* Converts ratings into numeric values.
* Converts rating counts into integers.
* Handles blank or invalid values.
* Inserts the cleaned records into the MySQL `Amazon` table.

## SQL Operations

The project demonstrates the following SQL concepts:

* `SELECT`
* `WHERE`
* `DISTINCT`
* `ORDER BY`
* `GROUP BY`
* `COUNT()`
* `AVG()`
* `HAVING`
* `BETWEEN`
* `LIKE`
* `CASE`

These operations are used to create separate tables for product analysis and backup purposes.

## Project Structure

```text
ETL-Pipeline/
│
├── etl_pipeline.py
├── amazon.csv
├── workflow.png
├── assets/
│   └── mysql-workbench.png
└── README.md
```

## Notes

* The project uses `CREATE TABLE IF NOT EXISTS ... AS SELECT ...` to create the output tables.
* If a backup table already exists, rerunning the program will not automatically refresh its contents.
* Drop the existing backup tables or modify the SQL when you need to regenerate them.
* Keep `amazon.csv` in the correct location before running the program.
* Do not upload MySQL passwords or other credentials to GitHub.
* Commit the database changes after successful table creation.
* Close the MySQL cursor and connection after the ETL process is completed.

## License

Add a license here if you intend to share or reuse this project publicly.

## Author

**Atharva Bodhai**
GitHub: `bodhaiatharva098-ab0012`
