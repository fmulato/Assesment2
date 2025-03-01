"""
This module contains the logic for the quiz game. It manages the display of questions, options, and results.
It provides the following functionality:
1. Display question: Displays the current question and options on the screen.
2. Display result: Displays the result of the current question (correct or incorrect).
3. Determine quiz winner: Determines the winner of the quiz based on the scores of the players.
"""
from utils import Utils

class Logic():
    def __init__(self, gs):
        self.gs = gs

    def display_question(self):
        if self.gs.current_question_index < len(self.gs.selected_questions):
            self.gs.question_number, self.gs.question_data = self.gs.selected_questions[self.gs.current_question_index]
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
            self.determine_quiz_winner()
            for button in self.gs.option_buttons:
                button.grid_forget()
            self.gs.submit_button.grid_forget()
            self.gs.result_label.configure(text="")
            #self.gs.next_button.grid_forget()
            #self.gs.restart_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
            #self.gs.winner_label.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    def check_answer(self):
        """Check the selected answer."""
        selected_option = self.gs.options_var.get()
        _, question_data = self.gs.selected_questions[self.gs.current_question_index]
        correct_answer = question_data[7]

        for button in self.gs.option_buttons:
            button.configure(text_color="black")

        if int(selected_option) == correct_answer:
            self.gs.result_label.configure(text="Correct!", text_color="blue")
            self.gs.score_player1 += 10
            self.gs.score_player1_label.configure(text=f"Score: {self.gs.score_player1}")
            self.gs.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
        else:
            self.gs.result_label.configure(text="Incorrect!", text_color="red")
            self.gs.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
            if selected_option:
                self.gs.option_buttons[int(selected_option) - 1].configure(text_color="red")

        self.gs.submit_button.configure(state="disabled")
        #self.gs.next_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def next_question(self):
        """Move to the next question."""
        self.gs.current_question_index += 1
        self.gs.submit_button.configure(state="normal")
        self.gs.next_button.pack_forget()
        self.display_question()

    def restart_quiz(self):
        """Restart the quiz."""
        self.gs.score_player1 = 0
        self.gs.score_player1_label.configure(text=f"Score: {self.gs.score_player1}")
        self.gs.current_question_index = 0
        self.gs.selected_questions = Utils().select_random_elements(self.gs.questions)
        self.gs.winner_label.configure(text="")
        self.gs.winner_label.grid(pady=(20, 0))
        self.gs.restart_button.grid_forget()

        for i, button in enumerate(self.gs.option_buttons):
            button.grid(row=3 + i, column=0, padx=10, pady=10, sticky="ew")
            # Reset button text before updating
            button.configure(text="")

        self.gs.submit_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.gs.result_label.configure(text="")
        self.display_question()

    def determine_quiz_winner(self):
        if self.gs.score_player1 > self.gs.score_player2:
            self.gs.winner_label.configure(text=f"{self.gs.player1} ({self.gs.age1}) is the winner!", text_color="green")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print(f"{self.gs.player1_label} is the winner!")
        elif self.gs.score_player1 < self.gs.score_player2:
            self.gs.winner_label.configure(text=f"{self.gs.player2} ({self.gs.age2}) is the winner!", text_color="blue")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print("Player 2 is the winner!")
        else:
            self.gs.winner_label.configure(text="It's a tie! Both players are winners!", text_color="green")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print("It's a tie! Both players are winners!")