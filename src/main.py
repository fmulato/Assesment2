"""
this is the main file
"""
import gui
from database_management import DataBase

def app():
    DataBase().load_db_from_json("questions.json")
    gui.StartScreen()

if __name__ == "__main__":
    app()
