"""
Database Manager
What: Reusable class to handle all database operations
Why: So we don't repeat connection code in every script
How: Contains methods for connect, query, insert, stats
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class DatabaseManager:
    """
    Blueprint for database operations.
    Think of this as a toolbox for talking to our database.
    """

    def __init__(self):
        """
        Constructor - runs automatically when you create the object
        Sets connection and cursor to None (empty) initially
        """
        self.conn = None   # Will hold database connection
        self.cur = None    # Will hold cursor (query executor)

    def connect(self):
        """
        Opens connection to database
        Returns True if successful, False if failed
        """
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            # RealDictCursor makes results come back as dictionaries
            # Instead of: (1, "Wikipedia", "AI/ML")
            # You get: {"id": 1, "source": "Wikipedia", "category": "AI/ML"}
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """
        Closes connection to database
        Always call this when you're done!
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("🔌 Disconnected from database")

    def execute_query(self, query, params=None):
        """
        Runs a SELECT query and returns results
        query = the SQL query string
        params = values to insert into query (optional)
        """
        try:
            self.cur.execute(query, params)
            results = self.cur.fetchall()
            return results
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None

    def execute_update(self, query, params=None):
        """
        Runs INSERT/UPDATE/DELETE query
        commit() saves the change permanently
        rollback() cancels if something goes wrong
        """
        try:
            self.cur.execute(query, params)
            self.conn.commit()      # Save permanently
            return True
        except Exception as e:
            print(f"❌ Update error: {e}")
            self.conn.rollback()    # Cancel the change
            return False

    def get_all_datasets(self):
        """Fetch all datasets ordered by quality"""
        query = """
        SELECT id, source, category, quality_score, word_count
        FROM datasets
        ORDER BY quality_score DESC;
        """
        return self.execute_query(query)

    def get_datasets_by_category(self, category):
        """
        Fetch datasets filtered by category
        %s is a placeholder - psycopg2 replaces it safely
        """
        query = """
        SELECT id, source, content, quality_score
        FROM datasets
        WHERE category = %s
        ORDER BY quality_score DESC;
        """
        return self.execute_query(query, (category,))

    def get_dataset_with_tags(self, dataset_id):
        """Fetch one dataset with all its tags using JOIN"""
        query = """
        SELECT 
            d.id,
            d.source,
            d.category,
            d.quality_score,
            STRING_AGG(t.name, ', ') as tags
        FROM datasets d
        LEFT JOIN dataset_tags dt ON d.id = dt.dataset_id
        LEFT JOIN tags t ON dt.tag_id = t.id
        WHERE d.id = %s
        GROUP BY d.id, d.source, d.category, d.quality_score;
        """
        results = self.execute_query(query, (dataset_id,))
        # Return first result only (there's only one dataset)
        return results[0] if results else None

    def get_statistics(self):
        """Get all database statistics in one dictionary"""
        stats = {}

        # Total datasets
        result = self.execute_query("SELECT COUNT(*) as count FROM datasets;")
        stats['total_datasets'] = result[0]['count']

        # Total tags
        result = self.execute_query("SELECT COUNT(*) as count FROM tags;")
        stats['total_tags'] = result[0]['count']

        # Total tag links
        result = self.execute_query("SELECT COUNT(*) as count FROM dataset_tags;")
        stats['total_links'] = result[0]['count']

        # Average quality score
        result = self.execute_query("SELECT ROUND(AVG(quality_score), 2) as avg FROM datasets;")
        stats['avg_quality'] = result[0]['avg']

        # Total categories
        result = self.execute_query("SELECT COUNT(DISTINCT category) as count FROM datasets;")
        stats['categories'] = result[0]['count']

        return stats


# This block only runs when you execute THIS file directly
# NOT when another file imports DatabaseManager
if __name__ == "__main__":
    # Create object from our blueprint
    db = DatabaseManager()

    # Try to connect
    if db.connect():

        # Show statistics
        print("\n📊 Database Statistics:")
        stats = db.get_statistics()
        for key, value in stats.items():
            print(f"   {key}: {value}")

        # Show AI/ML datasets
        print("\n🤖 AI/ML Datasets:")
        ai_datasets = db.get_datasets_by_category('AI/ML')
        for dataset in ai_datasets:
            print(f"   - {dataset['source']} (Quality: {dataset['quality_score']})")

        # Show one dataset with tags
        print("\n🏷️  Dataset #1 with tags:")
        dataset = db.get_dataset_with_tags(1)
        if dataset:
            print(f"   Source: {dataset['source']}")
            print(f"   Category: {dataset['category']}")
            print(f"   Tags: {dataset['tags']}")

        # Always disconnect when done
        db.disconnect()