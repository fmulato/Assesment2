#Still working on it till Sunday

import sqlite3
from datetime import datetime
from tkinter import messagebox, simpledialog

#databse files path
DB_PATH = "users.db"
QUIZ_DB_PATH = "quiz.db"


class UserManagement:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        # creating two tables
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                "id_player"	TEXT NOT NULL,
                "username"	TEXT NOT NULL UNIQUE,
                "birthday"	TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Scores (
                "id_player"	TEXT,
                "id_score"	INTEGER,
                "date_time"	TEXT,
                "age"	INTEGER,
                "current_score"	INTEGER
            );
        """)
        connection.commit()
        connection.close()

    def register_user(self, username, birthday):
        # adding new user to the database (players)
        try:
            birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return False

        id_player = username

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO players (id_player, username, birthday) VALUES (?, ?, ?)",
                           (id_player, username, birth_date))
            connection.commit()
            messagebox.showinfo("Success", f"User {username} registered successfully!")
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Try a different one.")
            return False
        finally:
            connection.close()

    def calculate_age(self, birthday):
        # calculating current age based the birthday
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def check_and_create_quiz_db(self):
        # if there's no quiz.db file, create new one
        if not os.path.exists(QUIZ_DB_PATH):
            connection = sqlite3.connect(QUIZ_DB_PATH)
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE "questions" (
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
