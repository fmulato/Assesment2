"""
This is the main file. It is responsible for starting the application by
calling the StartScreen class from the gui module.
The database is loaded from a JSON file and the questions are inserted
into the database.
"""
import gui
from database_management import DataBase

def app():
    """Start the application."""
    DataBase().load_db_from_json("questions.json")
    gui.StartScreen()

if __name__ == "__main__":
    """Start the application."""
    app()
