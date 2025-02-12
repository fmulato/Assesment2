import flet as ft
import json


def load_questions(file_path):
    """Load questions from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def main(page: ft.Page):
    page.title = "Quiz Game for Kids"
    page.window_width = 600
    page.window_height = 300

    questions = load_questions("questions.json")
    current_question_index = 0
    score = 0  # Variable to track the score
    selected_option = ft.Ref[ft.RadioGroup]()
    question_label = ft.Text("Question will appear here", size=16)
    score_label = ft.Text(f"Score: {score}", size=16)  # Display score

    option_buttons = ft.RadioGroup(content=ft.Column(), ref=selected_option)
    submit_button = ft.ElevatedButton("Submit")
    result_label = ft.Text("", size=16)  # Text label for displaying results

    def display_question():
        nonlocal current_question_index
        if current_question_index < len(questions):
            question_data = questions[current_question_index]
            question_label.value = question_data['question']

            option_buttons.content.controls.clear()
            for i, option in enumerate(question_data['options']):
                option_buttons.content.controls.append(
                    ft.Radio(value=str(i + 1), label=option)
                )
            page.update()
        else:
            question_label.value = "No more questions!"
            option_buttons.visible = False
            submit_button.visible = False
            page.update()

    def check_answer(e):
        nonlocal current_question_index, score
        if selected_option.current.value == questions[current_question_index]['correct_answer']:
            result_label.value = "Correct!"
            score += 10  # Add 10 points for correct answer
        else:
            result_label.value = "Incorrect!"

        # Update the score display
        score_label.value = f"Score: {score}"

        # Update the page and display feedback
        page.update()

        current_question_index += 1
        display_question()

    submit_button.on_click = check_answer

    page.add(
        ft.Column([
            question_label,
            option_buttons,
            submit_button,
            result_label,
            score_label  # Display score on the page
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    display_question()



