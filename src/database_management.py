"""
This module manages user data, players and quiz questions in a SQLite database using the sqlite3 library.
It provides the following functionality:
1. Database setup: Creates tables for players, scores, and questions if they do not exist in the database.
2. User registration: Adds a new user to the database with a unique username and birthday.
3. Age calculation: Calculates the age of a user based on their birthday.
4. Age saving: Saves the user's age in the scores table.
5. Quiz database creation: Creates a table for quiz questions if it does not exist.
6. Player retrieval: Fetches all players and their latest recorded age from the scores table.
7. JSON data loading: Loads questions into the database from a JSON file.
8. Question existence check: Checks if a question already exists in the database.
9. Question loading: Fetches all questions from the database.
"""

import sqlite3
import json
from datetime import datetime
from utils import CustomPopup
import sql_statement as sql_st

#databse files path
DB_PATH = "brainup.db"

class DataBase:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        """ Creates tables for players, scores, and questions if they do not exist in brainup.db. """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(sql_st.CREATE_TABLE_PLAYERS)
        cursor.execute(sql_st.CREATE_TABLE_SCORES)
        cursor.execute(sql_st.CREATE_TABLE_QUESTIONS)

        connection.commit()
        connection.close()

    def register_user(self, username, birthday):
        """ Adds a new user to the database. """
        try:
            birthday = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError as e:
            CustomPopup("Error", f"An error occurred: {e}")
            return False

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute(sql_st.CHECK_USERNAME, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            CustomPopup(self,"Error", "Username already exists. Try a different one.")
            return False

        try:
            cursor.execute(sql_st.INSERT_PLAYER, (username, birthday))
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
            cursor.execute(sql_st.SELECT_PLAYER_BY_USERNAME, (username,))
            result = cursor.fetchone()

            if result is None:
                CustomPopup("Error", f"User {username} not found in players table!")
                return False

            id_player = result[0]

            cursor.execute(sql_st.INSERT_AGE_TO_SCORES, (id_player, age))
            connection.commit()
            return True

        except sqlite3.Error as e:
            CustomPopup("Database Error", f"An error occurred: {e}")
            return False
        finally:
            connection.close()


    def get_all_players(self):
        """ Fetch all players and their latest recorded age from the scores table. """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(sql_st.SELECT_ALL_PLAYERS_WITH_AGE)
        players = cursor.fetchall()

        connection.close()

        return players

    def load_db_from_json(self, json_file):
        """Load questions into the database from a JSON file."""

        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File {json_file} not found.")
            return
        except json.JSONDecodeError:
            print("Error: File JSON is invalid.")
            return

        conn = sqlite3.connect('brainup.db')
        cursor = conn.cursor()
        n_questions_loaded = 0

        for item in data:
            category = item['category']
            question = item['question']
            options = item['options']
            correct_answer = int(item['correct_answer'])

            # before insert check if question already exists
            if self.check_if_question_exists(question):
                print(f"Question '{question}' already exists in the database.")
                continue

            cursor.execute(sql_st.INSERT_QUESTIONS, (category, question, options[0], options[1], options[2], options[3], correct_answer))

            n_questions_loaded += 1

        conn.commit()
        conn.close()

        print(f"{n_questions_loaded} questions loaded into the database!")

    def check_if_question_exists(self, question):
        """Check if a question already exists in the database."""
        conn = sqlite3.connect('brainup.db')
        cursor = conn.cursor()

        cursor.execute(sql_st.CHECK_IF_QUESTION_EXISTS, (question,))
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result is not None

    def load_questions(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(sql_st.SELECT_ALL_QUESTIONS)
        questions = cursor.fetchall()

        connection.close()

        return questions

    def get_ranking(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(sql_st.SELECT_RANKING)
        ranking = cursor.fetchall()

        connection.close()

        return ranking


