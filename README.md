Database Metadata Extractor

A Python tool to extract full database structure, including tables, columns, foreign key relationships, and generate both JSON and human-readable summaries.

This project was designed for MySQL databases and can help developers, analysts, or data engineers quickly understand complex schemas. Easy for prompt structuring to get the best out of AI Chatbots.

Features

Connects to a MySQL database using credentials you provide.

Fetches all tables in the database.

Extracts columns with metadata:

Field name

Data type

Nullable

Key

Default value

Extra info

Comments

Extracts foreign key relationships between tables.

Generates stored procedure information (optional enhancement).

Creates:

db_structure.json → full metadata in JSON format.

db_summary.txt → human-readable paragraph-style summary.

Fully compatible with Python 3.11+.

Handles Unicode output (UTF-8) for relations and special characters.

Installation

Clone this repository:
```
git clone <repo_url>
cd <repo_folder>

```
Create a Python virtual environment (optional but recommended):
```
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate # macOS/Linux
```

Install dependencies:
```
pip install pymysql
```

Usage

Open tablepython.py.

Update the DB_CONFIG dictionary with your database credentials:

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "your_database",
    "port": 3306
}


Run the script:
```
python tablepython.py
```

Outputs:
```
db_structure.json → structured JSON of tables, columns, and foreign keys.

db_summary.txt → paragraph-style summary of tables and their relationships.
```
