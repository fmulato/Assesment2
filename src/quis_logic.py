import json
from utils import select_random_elements
import datetime

class Logic():
    def __init__(self, gui):
        self.gui = gui

    def display_question(self):
        if self.gui.current_question_index < len(self.gui.selected_questions):
            self.gui.question_number, self.gui.question_data = self.gui.selected_questions[
                self.gui.current_question_index]
            self.gui.category_label.configure(text=f"Category: {self.gui.question_data['category']}")
            self.gui.question_label.configure(
                text=f"{self.gui.current_question_index + 1}. {self.gui.question_data['question']}")

            for i, option in enumerate(self.gui.question_data["options"]):
                self.gui.option_buttons[i].configure(text=option, text_color="black")
                self.gui.option_buttons[i]._value = str(i + 1)

            self.gui.options_var.set(None)
            self.gui.result_label.configure(text="")
            self.gui.next_button.pack_forget()
        else:
            self.gui.question_label.configure(text="No more questions!")
            self.determine_quiz_winner()
            for button in self.gui.option_buttons:
                button.pack_forget()
            self.gui.submit_button.pack_forget()
            self.gui.result_label.configure(text="")
            self.gui.next_button.pack_forget()
            self.gui.restart_button.pack(side="left", padx=10)
            self.gui.winner_label.pack(pady=(20, 0))