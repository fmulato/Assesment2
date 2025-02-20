#Still working on it till Sunday

import sqlite3
from tkinter import messagebox

#Path of userdb
DB_PATH = "users.db"  #


class UserManagement:
    def __init__(self):
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL CHECK(length(username) <= 18), 
                password TEXT NOT NULL CHECK(length(password) <= 18),
                age INTEGER NOT NULL CHECK(age BETWEEN 10 AND 12),
                current_score INTEGER NOT NULL DEFAULT 0,    
                total_score INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.commit()
        connection.close()

    def register_user(self, username, age):
        if not username or not age.isdigit():
            messagebox.showerror("Error", "Invalid input. Please enter a valid name and age.")
            return False

        age = int(age)
        if not (10 <= age <= 12):
            messagebox.showerror("Error", "Wrong age. Please enter your age again.")
            return False

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)",
                           (username, "default123", age))
            connection.commit()
            messagebox.showinfo("Success", f"User {username} registered successfully!")
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Try a different one.")
            return False
        finally:
            connection.close()