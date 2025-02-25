"""
This module contains utility functions to load questions into the database from a JSON file.
Verifies if a question already exists in the database. If it does, it skips the insertion.
"""""
import json
import sqlite3

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

if __name__ == "__main__":
    Utils().load_db_from_json('questions.json')

