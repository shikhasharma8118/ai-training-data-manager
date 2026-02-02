"""
Show database statistics - Using ONLY basic Python
Just calculations and print statements
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

print("=== DATABASE STATISTICS ===\n")

# Total datasets
cur.execute("SELECT COUNT(*) FROM datasets;")
total_datasets = cur.fetchone()[0]
print(f"📊 Total Datasets: {total_datasets}")

# Total tags
cur.execute("SELECT COUNT(*) FROM tags;")
total_tags = cur.fetchone()[0]
print(f"🏷️  Total Tags: {total_tags}")

# Average quality
cur.execute("SELECT AVG(quality_score) FROM datasets;")
avg_quality = cur.fetchone()[0]
print(f"⭐ Average Quality: {round(avg_quality, 2)}/10")

# Count by category
print("\n=== DATASETS BY CATEGORY ===")
cur.execute("""
    SELECT category, COUNT(*) as count
    FROM datasets
    GROUP BY category
    ORDER BY count DESC;
""")

categories = cur.fetchall()
for cat in categories:
    print(f"{cat[0]}: {cat[1]} datasets")

# Most popular tags
print("\n=== MOST POPULAR TAGS ===")
cur.execute("""
    SELECT t.name, COUNT(dt.dataset_id) as usage
    FROM tags t
    LEFT JOIN dataset_tags dt ON t.id = dt.tag_id
    GROUP BY t.name
    ORDER BY usage DESC
    LIMIT 5;
""")

tags = cur.fetchall()
for tag in tags:
    print(f"{tag[0]}: used {tag[1]} times")

# Close
cur.close()
conn.close()