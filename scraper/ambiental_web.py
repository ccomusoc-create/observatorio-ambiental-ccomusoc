import sqlite3
import pandas as pd
import os

DB_FILE = "data/ambiental.db"
CSV_FILE = "data/ambiental.csv"

os.makedirs('data', exist_ok=True)

conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM noticias ORDER BY fecha DESC", conn)
conn.close()

df.to_csv(CSV_FILE, index=False)
print("CSV actualizado para la web.")
