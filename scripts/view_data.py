"""
View database data - Using ONLY basic Python
Just print to terminal, no file operations
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

print("=== AI TRAINING DATASETS ===\n")

# Get all datasets
cur.execute("""
    SELECT id, source, category, quality_score, word_count
    FROM datasets
    ORDER BY quality_score DESC
    LIMIT 10;
""")

results = cur.fetchall()

# Print each dataset
for row in results:
    dataset_id = row[0]
    source = row[1]
    category = row[2]
    quality = row[3]
    words = row[4]
    
    print(f"ID: {dataset_id}")
    print(f"Source: {source}")
    print(f"Category: {category}")
    print(f"Quality: {quality}/10")
    print(f"Words: {words}")
    print("-" * 40)

# Close
cur.close()
conn.close()