# src/db/insert_to_db.py

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# ---- Load environment variables ----
load_dotenv(dotenv_path='.env')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME')

# Validate
if not all([DB_USER, DB_PASS, DB_NAME]):
    raise EnvironmentError("Please set DB_USER, DB_PASS, and DB_NAME in .env")

# --- Safely URL-encode password ---
ENCODED_PASS = quote_plus(DB_PASS)

# Build secure connection URL
DB_URL = f"postgresql+psycopg2://{DB_USER}:{ENCODED_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DB_URL)

# CSV path
CSV_PATH = 'data/clean/reviews_sentiment_themes_topic.csv'
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

# Read CSV
df = pd.read_csv(CSV_PATH)

# Bank name mapping
name_map = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "Dashen": "Dashen Bank"
}

# Load bank_id values from DB
banks_df = pd.read_sql("SELECT bank_id, bank_name FROM banks", engine)
bank_map = dict(zip(banks_df['bank_name'], banks_df['bank_id']))

# Build rows to insert
rows = []
for _, r in df.iterrows():
    bank_label = r.get("bank")
    bank_name = name_map.get(bank_label, bank_label)
    bank_id = bank_map.get(bank_name)

    if bank_id is None:
        continue

    sent_label = r.get("sent_label") if pd.notna(r.get("sent_label")) else r.get("sentiment_vader")
    sent_score = r.get("sent_score") if pd.notna(r.get("sent_score")) else r.get("vader_compound")

    rows.append((
        int(bank_id),
        r.get("review"),
        int(r.get("rating")) if pd.notna(r.get("rating")) else None,
        r.get("date"),
        sent_label,
        float(sent_score) if pd.notna(sent_score) else None,
        r.get("theme_primary"),
        r.get("source") if pd.notna(r.get("source")) else "google_play"
    ))

# Insert SQL
insert_sql = text("""
    INSERT INTO reviews 
    (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, theme_primary, source)
    VALUES (:bank_id, :review_text, :rating, :review_date, :sentiment_label, :sentiment_score, :theme_primary, :source)
""")

# Insert into DB
with engine.begin() as conn:
    for row in rows:
        conn.execute(insert_sql, {
            "bank_id": row[0],
            "review_text": row[1],
            "rating": row[2],
            "review_date": row[3],
            "sentiment_label": row[4],
            "sentiment_score": row[5],
            "theme_primary": row[6],
            "source": row[7]
        })

print(f"Inserted {len(rows)} rows into the 'reviews' table successfully.")
