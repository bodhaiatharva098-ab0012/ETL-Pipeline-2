Amazon Product ETL Pipeline with Python & MySQL

A beginner-friendly ETL (Extract, Transform, Load) project that uses Python and MySQL to process Amazon product data from a CSV file. The pipeline extracts raw product data, cleans and transforms it using Python, loads it into MySQL, and performs 12 SQL operations for analysis.

Overview

The pipeline uses mysql-connector-python to connect Python with MySQL. It reads amazon.csv, cleans fields such as prices, discount percentages, ratings, and rating counts, and loads the processed records into an Amazon table.

After loading the data, the program creates 12 separate backup/result tables using SQL operations such as WHERE, DISTINCT, ORDER BY, GROUP BY, COUNT, AVG, HAVING, BETWEEN, LIKE, and CASE.

ETL Workflow
Extract Amazon product data from amazon.csv.
Transform prices, discounts, ratings, and rating counts using Python.
Load the cleaned data into the MySQL Amazon table.
Transform and analyze the loaded data using SQL queries.
Store each SQL result in a separate backup/result table.
ETL Flow
Amazon CSV
    ↓
Python CSV Reader
    ↓
Data Cleaning & Transformation
    ↓
MySQL Database
    ↓
Amazon Table
    ↓
12 SQL Operations
    ↓
Backup / Result Tables
    ↓
Data Analysis
Tables Created
Table	SQL Operation
Backup_All	Select all Amazon records
Backup_High_Rating	Filter products with rating ≥ 4
Backup_Selected_Columns	Select specific product columns
Backup_Categories	Find distinct categories
Backup_Rating_Sorted	Sort products by rating
Backup_Category_Count	Count records by category
Backup_Average_Rating	Calculate average rating by category
Backup_High_Average_Rating	Filter categories with average rating ≥ 4
Backup_Price_Range	Filter prices between 500 and 5000
Backup_Selected_Categories	Filter selected product categories
Backup_Name_Search	Search product names containing Cable
Backup_Rating_Category	Categorize ratings using CASE

The program creates these result tables from the Amazon source table.

Screenshots
ETL Workflow https://github.com/bodhaiatharva098-ab0012/ETL-Pipeline-2/blob/main/Etl%20pipeline%202.jpg

MySQL Workbench Results

Place the workflow image in the repository as workflow.png and the MySQL Workbench screenshot as assets/mysql-workbench.png. Update the filenames if your actual image names are different.

Requirements
Python 3
MySQL Server
MySQL Workbench
VS Code
mysql-connector-python

Install the MySQL connector:

python -m pip install mysql-connector-python
Project Structure
Amazon-ETL-Pipeline/
│
├── hw etl.py
├── amazon.csv
├── workflow.png
├── assets/
│   └── mysql-workbench.png
└── README.md
Configure MySQL

Update the MySQL connection details in the Python program according to your local MySQL setup.

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="etl"
)

Do not upload your actual MySQL password to GitHub.

Run the Project
Start MySQL Server.
Make sure amazon.csv is in the same folder as hw etl.py.
Install the required Python package:
python -m pip install mysql-connector-python
Run the program:
python "hw etl.py"
Open MySQL Workbench and check the etl database and generated result tables.
Data Cleaning

The Python program performs basic data cleaning before inserting records into MySQL:

Removes ₹ and commas from prices.
Removes % from discount percentages.
Converts ratings into numeric values.
Removes commas from rating counts.
Handles empty or invalid numeric values.
SQL Analysis

The project demonstrates common SQL concepts including:

SELECT
WHERE
DISTINCT
ORDER BY
GROUP BY
COUNT()
AVG()
HAVING
BETWEEN
LIKE
CASE

This makes the project useful for learning Python, SQL, MySQL, ETL, and basic data engineering concepts.

Output

After successful execution, the program:

Loads the CSV data into MySQL.
Creates the 12 analysis/result tables.
Commits the database changes.
Displays the total number of records.
Displays the tables created in the database.
Closes the MySQL connection.
Author

Atharva Bodhai

Project Title

Amazon Product ETL Pipeline using Python and MySQL
