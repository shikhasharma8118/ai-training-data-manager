"""
Add a new dataset - Using ONLY basic Python
No file operations, just direct insert
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Connect
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cur = conn.cursor()

# Sample new dataset
new_content = "Artificial intelligence is transforming healthcare with diagnostic tools and treatment planning."
new_source = "Medical Journal"
new_category = "AI/ML"
new_quality = 8
new_word_count = 13

# Insert query
insert_query = """
INSERT INTO datasets (content, source, category, quality_score, word_count)
VALUES (%s, %s, %s, %s, %s)
RETURNING id;
"""

# Execute
cur.execute(insert_query, (new_content, new_source, new_category, new_quality, new_word_count))

# Get the ID of inserted row
new_id = cur.fetchone()[0]

# Commit the transaction
conn.commit()

print("✅ Dataset added successfully!")
print(f"📊 New dataset ID: {new_id}")
print(f"Source: {new_source}")
print(f"Category: {new_category}")

# Close
cur.close()
conn.close()