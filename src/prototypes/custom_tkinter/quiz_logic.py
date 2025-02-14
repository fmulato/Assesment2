import json
import random
class Logic():
    def __init__(self, gui):
        self.gui = gui

    def load_questions(self, file_path):
        """Load questions from a JSON file."""
        with open(file_path, "r", encoding='utf-8') as file:
            questions = json.load(file)
        return questions

    def display_question(self):
        """Exibe a questão atual na interface."""
        if self.gui.current_question_index < len(self.gui.selected_questions):
            self.gui.question_number, self.gui.question_data = self.gui.selected_questions[self.gui.current_question_index]
            self.gui.category_label.configure(text=f"Category: {self.gui.question_data['category']}")
            self.gui.question_label.configure(text=f"{self.gui.current_question_index + 1}. {self.gui.question_data['question']}")
            for i, option in enumerate(self.gui.question_data["options"]):
                self.gui.option_buttons[i].configure(text=option, text_color="black")
                self.gui.option_buttons[i]._value = str(i + 1)
            self.gui.options_var.set(None)
            self.gui.result_label.configure(text="")
            self.gui.next_button.pack_forget()
        else:
            self.gui.question_label.configure(text="No more questions!")
            for button in self.gui.option_buttons:
                button.pack_forget()
            self.gui.submit_button.pack_forget()
            self.gui.result_label.configure(text="")
            self.gui.next_button.pack_forget()
            self.gui.restart_button.pack(pady=20)

    def check_answer(self):
        """Check the selected answer."""
        selected_option = self.gui.options_var.get()
        _, question_data = self.gui.selected_questions[self.gui.current_question_index]
        correct_answer = question_data["correct_answer"]

        # Reset option colours
        for button in self.gui.option_buttons:
            button.configure(text_color="black")

        if selected_option == correct_answer:
            # Correct answer
            self.gui.result_label.configure(text="Correct!", text_color="blue")
            self.gui.score_player1 += 10
            self.gui.score_player1_label.configure(text=f"Score: {self.gui.score_player1}")
            # Highlight the correct option in blue
            self.gui.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
        else:
            # Incorrect answer
            self.gui.result_label.configure(text="Incorrect!", text_color="red")
            # Highlight the correct option in blue
            self.gui.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
            # Highlight the selected option in red
            if selected_option:
                self.gui.option_buttons[int(selected_option) - 1].configure(text_color="red")

        # Disable the Submit button and show the Next button
        self.gui.submit_button.configure(state="disabled")
        self.gui.next_button.pack(side="top", anchor='center', padx=10)

    def next_question(self):
        """Move to the next question."""
        self.gui.current_question_index += 1
        self.gui.submit_button.configure(state="normal")  # Re-enable the Submit button
        self.gui.next_button.pack_forget()  # Hide the Next button
        self.display_question()

    def restart_quiz(self):
        """Restart the quiz."""
        self.gui.score_player1 = 0
        self.gui.score_player1_label.configure(text=f"Score: {self.gui.score_player1}")
        self.gui.current_question_index = 0
        self.gui.selected_questions = random.sample(list(enumerate(self.gui.questions, start=1)), 3)  # Select 3 random questions
        self.gui.restart_button.pack_forget()  # Hide the restart button

        # Re-display the option buttons and Submit button
        for button in self.gui.option_buttons:
            button.pack(anchor="w", padx=20, pady=5)
        self.gui.submit_button.pack(side="top", anchor='center', padx=10)
        self.gui.result_label.configure(text="")  # Clear the previous result

        self.display_question()  # Display the first question