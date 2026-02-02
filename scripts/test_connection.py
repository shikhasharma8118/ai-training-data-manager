"""
Test database connection - Using ONLY basic Python
No file handling, no pandas, just basics!
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Show what we loaded (hide password)
print("=== Testing Connection ===")
print(f"Host: {host}")
print(f"Port: {port}")
print(f"Database: {database}")
print(f"User: {user}")
print(f"Password: {'***' if password else 'NOT SET'}")
print()

# Try to connect
try:
    # Connect to database
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    # Create cursor
    cur = conn.cursor()
    
    # Run simple query
    cur.execute("SELECT COUNT(*) FROM datasets;")
    count = cur.fetchone()[0]
    
    print("✅ SUCCESS! Connected to database")
    print(f"📊 Total datasets: {count}")
    
    # Close
    cur.close()
    conn.close()
    
except Exception as e:
    print("❌ FAILED! Could not connect")
    print(f"Error: {e}")