import sqlite3
import os
from datetime import datetime
import customtkinter as ctk

#databse files path
DB_PATH = "brainup.db"
#DB_PATH = "users.db"
#QUIZ_DB_PATH = "quiz.db"

class UserManagement:
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
                "birthday" TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scores (
                "id_score" INTEGER PRIMARY KEY AUTOINCREMENT,
                "id_player" INTEGER,
                "date_time" TEXT DEFAULT CURRENT_TIMESTAMP,
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
            birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            CustomPopup("Error", "Invalid date format. Use YYYY-MM-DD.")
            return False

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM players WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            CustomPopup("Error", "Username already exists. Try a different one.")
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

    def calculate_age(self, birthday):
        """ Calculate age from birth date. """
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

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
            SELECT p.username, COALESCE(s.age, (SELECT age FROM scores WHERE id_player = p.id_player ORDER BY date_time DESC LIMIT 1)) 
            FROM players p 
            LEFT JOIN scores s ON p.id_player = s.id_player 
            GROUP BY p.username
        """
        cursor.execute(query)
        players = cursor.fetchall()

        connection.close()

        return players


class CustomPopup(ctk.CTkToplevel):
    """ Custom pop-up window for success and error messages """
    def __init__(self, title, message):
        super().__init__()
        self.title(title)

        from gui import RootUtils

        gui = RootUtils()
        window_width = 300
        window_height = 150
        gui.center_window(self, window_width, window_height)

        #self.geometry("300x150")
        self.grab_set()  # Make modal

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=10)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)

