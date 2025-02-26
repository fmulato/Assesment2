"""
This module contains the logic for the quiz game. It manages the display of questions, options, and results.
It provides the following functionality:
1. Display question: Displays the current question and options on the screen.
2. Display result: Displays the result of the current question (correct or incorrect).
3. Determine quiz winner: Determines the winner of the quiz based on the scores of the players.
"""

class Logic():
    def __init__(self, gs):
        self.gs = gs

    def display_question(self):
        if self.gs.current_question_index < len(self.gs.selected_questions):
            self.gs.question_number, self.gs.question_data = self.gs.selected_questions[self.gs.current_question_index]
            print(self.gs.question_number)
            print(self.gs.question_data[1])

            self.gs.category_label.configure(text=f"Category: {self.gs.question_data[1]}")
            self.gs.question_label.configure(
                text=f"{self.gs.current_question_index + 1}. {self.gs.question_data[2]}")

            for i, option in enumerate(self.gs.question_data[3:7]):
                self.gs.option_buttons[i].configure(text=option, text_color="black")
                self.gs.option_buttons[i]._value = str(i + 1)

            self.gs.options_var.set(None)
            self.gs.result_label.configure(text="")
            #self.gs.next_button.grid_forget()
        else:
            self.gs.question_label.configure(text="No more questions!")
            #self.determine_quiz_winner()
            for button in self.gs.option_buttons:
                button.grid_forget()
            self.gs.submit_button.grid_forget()
            self.gs.result_label.configure(text="")
            #self.gs.next_button.grid_forget()
            #self.gs.restart_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
            #self.gs.winner_label.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

