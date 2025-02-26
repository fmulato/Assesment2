"""
This module contains utility functions to load questions into the database from a JSON file.
Verifies if a question already exists in the database. If it does, it skips the insertion.
"""""
import json
import sqlite3
import random
from typing import Sequence, List, Tuple
import customtkinter as ctk
from datetime import datetime

NUMBER_QUESTION = 3

class Utils:

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

            cursor.execute("""
            INSERT INTO questions (category, question, option_1, option_2, option_3, option_4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (category, question, options[0], options[1], options[2], options[3], correct_answer))

            n_questions_loaded += 1

        conn.commit()
        conn.close()

        print(f"{n_questions_loaded} questions loaded into the database!")

    def check_if_question_exists(self, question):
        """Check if a question already exists in the database."""
        conn = sqlite3.connect('brainup.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM questions WHERE question = ?", (question,))
        result = cursor.fetchone()

        conn.close()

        return result is not None



    def select_random_elements(elements: Sequence, n: int = NUMBER_QUESTION) -> List[Tuple[int, any]]:

        if not isinstance(elements, (list, tuple, set)):
            raise ValueError("The 'elements' argument must be a list, tuple, or set.")

        elements = list(elements)  # Ensures it is a list to support indexing

        if n > len(elements):
            raise ValueError("The number of selected elements (m) cannot be greater than the total elements (n).")

        return random.sample(list(enumerate(elements, start=1)), n)

    def calculate_age(self, birthday):
        """ Calculate age from birth date. """
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


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

        self.grab_set()  # Make modal

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=10)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)


