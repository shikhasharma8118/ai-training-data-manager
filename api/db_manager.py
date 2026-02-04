"""
Database Manager - Complete version for FastAPI
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self):
        """Initialize connection variables"""
        self.conn = None
        self.cur = None

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ Database connected")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("🔌 Database disconnected")

    def execute_query(self, query, params=None):
        """
        Execute any SQL query and return results
        Handles both SELECT and INSERT/UPDATE/DELETE with RETURNING
        """
        try:
            self.cur.execute(query, params)
            
            # Check if query modifies data (INSERT, UPDATE, DELETE)
            query_upper = query.strip().upper()
            if query_upper.startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.conn.commit()  # Save changes to database
                print("✅ Changes committed to database")
            
            # Return results if query returns rows
            if self.cur.description:
                results = self.cur.fetchall()
                return results
            
            return None
            
        except Exception as e:
            print(f"❌ Query error: {e}")
            if self.conn:
                self.conn.rollback()  # Undo changes on error
            raise e  # Re-raise so FastAPI can catch it

    def get_all_datasets(self):
        """Get all datasets ordered by quality score"""
        query = """
        SELECT id, source, category, quality_score, word_count
        FROM datasets
        ORDER BY quality_score DESC;
        """
        return self.execute_query(query)

    def get_statistics(self):
        """Get database statistics"""
        stats = {}
        
        # Total datasets
        result = self.execute_query("SELECT COUNT(*) as count FROM datasets;")
        stats['total_datasets'] = result[0]['count'] if result else 0
        
        # Total tags
        result = self.execute_query("SELECT COUNT(*) as count FROM tags;")
        stats['total_tags'] = result[0]['count'] if result else 0
        
        return stats