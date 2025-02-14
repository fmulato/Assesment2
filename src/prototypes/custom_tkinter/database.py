import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def create_db(self):
        """Create a new SQLite database."""
        pass

    def db_exists(self):
        """Check if the database already exists."""
        pass

    def load_db_from_json(self, json_file):
        """Load data into the database from a JSON file."""
        pass

    def fetch_questions(self):
        """Fetch questions from the database."""
        pass

    def close_connection(self):
        """Close the database connection."""
        pass