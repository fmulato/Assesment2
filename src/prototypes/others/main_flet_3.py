import flet as ft
from quiz_logic import QuizManager
from ui_components import UIManager

# Constants
SIZE_WIDTH = 1000
SIZE_HEIGHT = 600

def main(page: ft.Page):
    page.title = "Quiz Game for Kids"
    page.window_width = SIZE_WIDTH
    page.window_height = SIZE_HEIGHT
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Initialize QuizManager and UIManager
    quiz_manager = QuizManager("questions.json")
    ui_manager = UIManager(page, quiz_manager)

    # Display the first question
    ui_manager.display_question()

    # Add the main layout to the page
    page.add(ui_manager.build_layout())

if __name__ == "__main__":
    ft.app(target=main)