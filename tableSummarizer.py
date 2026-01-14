import pymysql
import json
import sys
import os

DB_CONFIG = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "port": 3306,
}

print("Attempting connection...")
try:
    conn = pymysql.connect(**DB_CONFIG)
    print("Connected.")
except Exception as e:
    print("Failed to connect:", e)
    sys.exit(1)

cursor = conn.cursor()

def fetch_tables():
    print("Fetching tables...")
    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    tables = [r[0] for r in rows]
    print(f"Found {len(tables)} tables: {tables}")
    return tables

def fetch_columns(table):
    cursor.execute(f"SHOW FULL COLUMNS FROM `{table}`")
    rows = cursor.fetchall()
    cols = []
    for r in rows:
        cols.append({
            "field": r[0],
            "type": r[1],
            "nullable": r[3],
            "key": r[4],
            "default": r[5],
            "extra": r[6],
            "comment": r[8] if len(r) > 8 else ""
        })
    return cols

def fetch_fk_constraints():
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME IS NOT NULL AND TABLE_SCHEMA = %s
    """, (DB_CONFIG["database"],))
    return cursor.fetchall()

tables = fetch_tables()

if not tables:
    print("⚠ No tables found in this database. Exiting.")
    sys.exit(0)

print("Fetching FK constraints...")
fk_info = fetch_fk_constraints()
fk_map = {}
for tbl, col, ref_tbl, ref_col in fk_info:
    fk_map.setdefault(tbl, []).append({
        "column": col,
        "references": f"{ref_tbl}.{ref_col}"
    })

    # Build relations list for relations.txt
relations = []
for tbl, col, ref_tbl, ref_col in fk_info:
    relations.append((tbl, col, ref_tbl, ref_col))
    fk_map.setdefault(tbl, []).append({
        "column": col,
        "references": f"{ref_tbl}.{ref_col}"
    })


metadata = {}
print("Processing metadata...")
for t in tables:
    metadata[t] = {
        "columns": fetch_columns(t),
        "foreign_keys": fk_map.get(t, [])
    }

cwd = os.getcwd()
print("Writing output to", cwd)

# Write relations (human readable)
with open("relations.txt", "w", encoding="utf-8") as f:
    for tbl, col, ref_tbl, ref_col in relations:
        f.write(f"{tbl}.{col} → {ref_tbl}.{ref_col}\n")

# Write JSON metadata (actual structure)
with open("db_structure.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("db_structure.json created.")

# Write summary (plain english)
with open("db_summary.txt", "w", encoding="utf-8") as f:
    for tbl, data in metadata.items():
        fields = [c["field"] for c in data["columns"]]
        f.write(f"Table '{tbl}' contains the fields: {', '.join(fields)}.\n")
        if data["foreign_keys"]:
            f.write("Relations: ")
            rel = [f"{fk['column']} → {fk['references']}" for fk in data["foreign_keys"]]
            f.write(", ".join(rel))
        f.write("\n\n")

    for tbl, data in metadata.items():
        fields = [c["field"] for c in data["columns"]]
        f.write(f"Table '{tbl}' contains the fields: {', '.join(fields)}.\n")
        if data["foreign_keys"]:
            f.write("Relations: ")
            rel = [f"{fk['column']} → {fk['references']}" for fk in data["foreign_keys"]]
            f.write(", ".join(rel))
        f.write("\n\n")


print("db_summary.txt created.")

cursor.close()
conn.close()
print("Done.")
