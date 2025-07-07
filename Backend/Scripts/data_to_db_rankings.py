import pandas as pd
import numbers
import sqlite3
from utils import normalize_name

# Load the CSV
df = pd.read_json("data/usnews_detailed_data.json")

# Make sure normalized name exists
# if "normalizedName" not in df.columns:
#     raise ValueError("Missing 'normalizedName' column in CSV")

# Connect to SQLite database
conn = sqlite3.connect("University_rankings.db")
cursor = conn.cursor()

# Columns to ignore (non-ranking data)
non_ranking_columns = {
    "Name", "normalizedName", "Country", "Country Code", "City", "Photo", "Blurb"
}

# Automatically find ranking columns
ranking_columns = [
    col for col in df.columns if col not in non_ranking_columns and df[col].dtype in [float, int]
]

print(f"🔍 Detected ranking columns: {ranking_columns}")

rows_inserted = 0

# Loop over each row in the DataFrame
for _, row in df.iterrows():
    normalized_name = normalize_name(row.get('Name'))
    for col in ranking_columns:
        rank_value = row[col]
        if pd.notna(rank_value):
            # Attempt to extract source and subject from column name
            parts = col.split("_", 1)
            if len(parts) == 2:
                source, subject = parts
            else:
                source, subject = "US_News", col
            if "SCORE" in subject or "Index" in subject:
                continue
            if not isinstance(rank_value, numbers.Number):
                continue
            print(normalized_name,source,subject,rank_value,sep=',')
            # Insert into the Rankings table
            try:
                cursor.execute("""
                    INSERT INTO Rankings (normalized_name, source, subject, rank_value)
                    VALUES (?, ?, ?, ?)
                """, (normalized_name, source, subject, rank_value))
                rows_inserted += 1
            except Exception as e:
                print(f"❌ Insert failed for {normalized_name} - {col}: {e}")

# Finalize
conn.commit()
conn.close()

print(f"✅ Inserted {rows_inserted} ranking rows into Rankings table.")
