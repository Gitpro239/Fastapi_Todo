import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///todos.db')
        self.db_path = self.database_url.replace('sqlite:///', '')
        self.init_db()
    
    def get_db_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Create todos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

# Create database instance
db = Database()


# import sqlite3
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_db_connection():
#     """Create and return a database connection"""
#     database_url = os.getenv('DATABASE_URL', 'sqlite:///todos.db')
#     # Extract database file path from URL
#     db_path = database_url.replace('sqlite:///', '')
#     conn = sqlite3.connect(db_path)
#     conn.row_factory = sqlite3.Row  # This enables column access by name
#     return conn

# def init_db():
#     """Initialize the database with required tables"""
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # Create todos table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS todos (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             description TEXT,
#             completed BOOLEAN NOT NULL DEFAULT 0,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# # Initialize database when module is imported
# init_db()
