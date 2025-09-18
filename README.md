SQL Query Parser

Overview

This repository contains a Python script designed to parse raw SQL query strings and extract a structured list of the tables and columns referenced within them. The primary goal is to provide a simple, dependency-free way to quickly analyze SQL code and understand which data entities are being used. The entire process is handled using Python's built-in regular expression library.

How It Works

The script operates by performing a series of logical steps to deconstruct and analyze the input SQL string:

1. Statement Separation

First, the script takes the full SQL string and splits it based on the semicolon (;) character. This allows it to process multiple, distinct SQL queries that might exist in a single block of text, handling each one individually.

2. Table Identification

For each individual query, a regular expression is used to find all table names. It specifically looks for words that immediately follow the FROM and JOIN keywords. This method effectively captures the primary table as well as any other tables being joined in the query. All identified tables are collected for the next step.

3. Column Extraction

Next, a second, more complex regular expression scans the entire query to find all potential column names. This pattern is designed to identify standalone words but also includes a negative lookahead to actively exclude common SQL keywords (like SELECT, GROUP, ORDER, CASE, etc.). This helps reduce noise and ensures the results are more likely to be actual column or alias names.

4. Data Structuring and Output
   
Finally, the script organizes the extracted data into a clear dictionary format. The table names are used as the keys. For each table, the script compiles a list of all the potential column names found in that query. To ensure there are no duplicates, it temporarily uses a set before converting the final list of columns, which is then sorted alphabetically.

The final output is a single dictionary containing all the tables found across all parsed statements and their associated columns.







