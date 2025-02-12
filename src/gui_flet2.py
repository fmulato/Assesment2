import flet as ft
import json

SIZE_WIDTH = 1000
SIZE_HEIGHT = 600

def load_questions(file_path):
    """Load questions from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def main(page: ft.Page):
    page.title = "Quiz Game for Kids"
    page.window_width = SIZE_WIDTH  # Define a largura da janela
    page.window_height = SIZE_HEIGHT  # Define a altura da janela
    page.window_resizable = False  # Impede que a janela seja redimensionada
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Centraliza os componentes verticais
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER  # Centraliza os componentes horizontais

    questions = load_questions("questions.json")
    current_question_index = 0
    score_player1 = 0  # Score of Player 1
    score_player2 = 0  # Static Score for Player 2
    selected_option = ft.Ref[ft.RadioGroup]()

    # Frames for layout without borders
    frame_left = ft.Column([
        ft.Text("Player 1", size=16),
        ft.Text(f"Score: {score_player1}", size=16, ref=ft.Ref())
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=0.2 * SIZE_WIDTH)  # 20% of WIDTH

    frame_right = ft.Column([
        ft.Text("Player 2", size=16),
        ft.Text(f"Score: {score_player2}", size=16)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=0.2 * SIZE_WIDTH)  # 20% of WIDTH

    frame_center = ft.Column([], alignment=ft.MainAxisAlignment.CENTER, spacing=20, width=0.6 * SIZE_WIDTH)  # 60% of WIDTH

    question_label = ft.Text("Question will appear here", size=16)
    option_buttons = ft.RadioGroup(content=ft.Column(), ref=selected_option)
    submit_button = ft.ElevatedButton("Submit")
    result_label = ft.Text("", size=16)

    frame_center.controls.append(question_label)
    frame_center.controls.append(option_buttons)
    frame_center.controls.append(submit_button)
    frame_center.controls.append(result_label)

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
        nonlocal current_question_index, score_player1
        if selected_option.current.value == questions[current_question_index]['correct_answer']:
            result_label.value = "Correct!"
            score_player1 += 10  # Add 10 points for correct answer

            # Update Player 1 score
            frame_left.controls[1].value = f"Score: {score_player1}"

        else:
            result_label.value = "Incorrect!"

        # Update the page and display feedback
        page.update()

        current_question_index += 1
        display_question()

    submit_button.on_click = check_answer

    # Layout with fixed widths for each frame
    # Layout with fixed widths for each frame and a separator
    page.add(
        ft.Row([
            frame_left,  # 20% width
            ft.VerticalDivider(),  # Separador vertical
            frame_center,  # 60% width
            ft.VerticalDivider(),  # Separador vertical
            frame_right  # 20% width
        ], alignment=ft.MainAxisAlignment.CENTER, width=SIZE_WIDTH, height=SIZE_HEIGHT,
            spacing=0,  # Sem espaço entre os frames
            expand=False)
    )

    display_question()

if __name__ == "__main__":
    ft.app(target=main)