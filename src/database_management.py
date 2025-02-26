"""
This module manages user data, players and quiz questions in a SQLite database using the sqlite3 library.
It provides the following functionality:
1. Database setup: Creates tables for players, scores, and questions if they do not exist in the database.
2. User registration: Adds a new user to the database with a unique username and birthday.
3. Age calculation: Calculates the age of a user based on their birthday.
4. Age saving: Saves the user's age in the scores table.
5. Quiz database creation: Creates a table for quiz questions if it does not exist.
6. Player retrieval: Fetches all players and their latest recorded age from the scores table.
"""

import sqlite3
from datetime import datetime
from utils import CustomPopup

#databse files path
DB_PATH = "brainup.db"

class DataBase:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        """ Creates tables for players, scores, and questions if they do not exist in brainup.db. """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                "id_player" INTEGER PRIMARY KEY AUTOINCREMENT,
                "username" TEXT NOT NULL UNIQUE,
                "birthday" DATE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scores (
                "id_score" INTEGER PRIMARY KEY AUTOINCREMENT,
                "id_player" INTEGER,
                "date_time" DATETIME DEFAULT CURRENT_TIMESTAMP,
                "age" INTEGER NOT NULL,
                "current_score" INTEGER DEFAULT 0,
                FOREIGN KEY (id_player) REFERENCES players(id_player) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS questions (
                "id_question" INTEGER PRIMARY KEY AUTOINCREMENT,
                "category" TEXT NOT NULL,
                "question" TEXT NOT NULL,
                "option_1" TEXT NOT NULL,
                "option_2" TEXT NOT NULL,
                "option_3" TEXT NOT NULL,
                "option_4" TEXT NOT NULL,
                "correct_answer" INTEGER NOT NULL
            );
        """)
        connection.commit()
        connection.close()

    def register_user(self, username, birthday):
        """ Adds a new user to the database. """
        try:
            birthday = datetime.strptime(birthday, "%Y-%m-%d")
            print(birthday)
        except ValueError as e:
            CustomPopup("Error", f"An error occurred: {e}")
            return False

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM players WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            CustomPopup(self,"Error", "Username already exists. Try a different one.")
            return False

        try:
            cursor.execute("INSERT INTO players (username, birthday) VALUES (?, ?)", (username, birthday))
            connection.commit()
            CustomPopup("Success", f"User {username} registered successfully!")
            return True
        except sqlite3.Error as e:
            CustomPopup("Database Error", f"An error occurred: {e}")
            return False
        finally:
            connection.close()



    def save_age_to_scores(self, username, age):
        """ Saves the user's age in the scores table using id_player. """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id_player FROM players WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result is None:
                CustomPopup("Error", f"User {username} not found in players table!")
                return False

            id_player = result[0]

            cursor.execute("INSERT INTO scores (id_player, age) VALUES (?, ?)", (id_player, age))
            connection.commit()
            return True
        except sqlite3.Error as e:
            CustomPopup("Database Error", f"An error occurred: {e}")
            return False
        finally:
            connection.close()

    def check_and_create_quiz_db(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                "id_question" INTEGER PRIMARY KEY AUTOINCREMENT,
                "category" TEXT NOT NULL,
                "question" TEXT NOT NULL,
                "option_1" TEXT NOT NULL,
                "option_2" TEXT NOT NULL,
                "option_3" TEXT NOT NULL,
                "option_4" TEXT NOT NULL,
                "correct_answer" INTEGER NOT NULL
            );
        """)
        connection.commit()
        connection.close()

    def get_all_players(self):
        """ Fetch all players and their latest recorded age from the scores table. """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = """
            SELECT username, 
                   (strftime('%Y', 'now') - strftime('%Y', birthday)) - 
                   (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age
            FROM 
                   players;
        """
        cursor.execute(query)
        players = cursor.fetchall()

        connection.close()

        #print("📋 Players in DB:", players)  # ✅ Debugging output

        return players




