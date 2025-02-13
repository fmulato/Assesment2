import flet as ft

class UIManager:
    def __init__(self, page, quiz_manager):
        self.page = page
        self.quiz_manager = quiz_manager
        self.selected_option = ft.Ref[ft.RadioGroup]()
        self.frame_left = self.create_frame_left()
        self.frame_right = self.create_frame_right()
        self.frame_center = self.create_frame_center()

    def create_frame_left(self):
        """Create the left frame for Player 1."""
        return ft.Column([
            ft.Text("Player 1", size=16),
            ft.Text(f"Score: {self.quiz_manager.score_player1}", size=16, ref=ft.Ref())
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=200)

    def create_frame_right(self):
        """Create the right frame for Player 2."""
        return ft.Column([
            ft.Text("Player 2", size=16),
            ft.Text(f"Score: {self.quiz_manager.score_player2}", size=16)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=200)

    def create_frame_center(self):
        """Create the center frame for questions and options."""
        self.question_label = ft.Text("Question will appear here", size=16)
        self.option_buttons = ft.RadioGroup(content=ft.Column(), ref=self.selected_option)
        self.submit_button = ft.ElevatedButton("Submit", on_click=self.check_answer)
        self.result_label = ft.Text("", size=16)

        return ft.Column([
            self.question_label,
            self.option_buttons,
            self.submit_button,
            self.result_label
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, width=600)

    def display_question(self):
        """Display the current question and options."""
        question_data = self.quiz_manager.get_current_question()
        if question_data:
            self.question_label.value = question_data['question']
            self.option_buttons.content.controls.clear()
            for i, option in enumerate(question_data['options']):
                self.option_buttons.content.controls.append(
                    ft.Radio(value=str(i + 1), label=option)
                )
        else:
            self.question_label.value = "No more questions!"
            self.option_buttons.visible = False
            self.submit_button.visible = False
        self.page.update()

    def check_answer(self, e):
        """Handle answer submission."""
        if self.quiz_manager.check_answer(self.selected_option.current.value):
            self.result_label.value = "Correct!"
        else:
            self.result_label.value = "Incorrect!"

        # Update Player 1 score
        self.frame_left.controls[1].value = f"Score: {self.quiz_manager.score_player1}"
        self.page.update()

        # Move to the next question
        self.quiz_manager.next_question()
        self.display_question()

    def build_layout(self):
        """Build the main layout with frames."""
        return ft.Row([
            self.frame_left,
            ft.VerticalDivider(),
            self.frame_center,
            ft.VerticalDivider(),
            self.frame_right
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)