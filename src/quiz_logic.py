import json
from utils import select_random_elements
import datetime

class Logic():
    def __init__(self, gui):
        self.gui = gui

    def load_questions(self, file_path):
        """Load questions from a JSON file."""
        with open(file_path, "r", encoding='utf-8') as file:
            questions = json.load(file)
        return questions

    def save_player_info(self):
        """Prompt for player name and age, then save to a JSON file with an ID and timestamp."""
        self.gui.player1_name = input("Enter player name: ")
        self.gui.player_age = input("Enter player age: ")
        self.gui.player_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.gui.timestamp = datetime.datetime.now().isoformat()

        # Update the player label
        self.gui.player1_label.configure(text=f"Player 1: {self.gui.player1_name}")

        player_data = {
            "id": self.gui.player1_name,
            "name": self.gui.player_age,
            "age": self.gui.player_id,
            "timestamp": self.gui.timestamp
        }

        try:
            with open("players.json", "r", encoding='utf-8') as file:
                players = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            players = []

        players.append(player_data)

        with open("players.json", "w", encoding='utf-8') as file:
            json.dump(players, file, indent=4)

        print("Player information saved successfully!")

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

    def check_answer(self):
        """Check the selected answer."""
        selected_option = self.gui.options_var.get()
        _, question_data = self.gui.selected_questions[self.gui.current_question_index]
        correct_answer = question_data["correct_answer"]

        for button in self.gui.option_buttons:
            button.configure(text_color="black")

        if selected_option == correct_answer:
            self.gui.result_label.configure(text="Correct!", text_color="blue")
            self.gui.score_player1 += 10
            self.gui.score_player1_label.configure(text=f"Score: {self.gui.score_player1}")
            self.gui.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
        else:
            self.gui.result_label.configure(text="Incorrect!", text_color="red")
            self.gui.option_buttons[int(correct_answer) - 1].configure(text_color="blue")
            if selected_option:
                self.gui.option_buttons[int(selected_option) - 1].configure(text_color="red")

        self.gui.submit_button.configure(state="disabled")
        self.gui.next_button.pack(side="left", padx=10)

    def next_question(self):
        """Move to the next question."""
        self.gui.current_question_index += 1
        self.gui.submit_button.configure(state="normal")
        self.gui.next_button.pack_forget()
        self.display_question()

    def restart_quiz(self):
        """Restart the quiz."""
        self.gui.score_player1 = 0
        self.gui.score_player1_label.configure(text=f"Score: {self.gui.score_player1}")
        self.gui.current_question_index = 0
        self.gui.selected_questions = select_random_elements(self.gui.questions)
        self.gui.winner_label.configure(text="")
        self.gui.winner_label.pack(pady=(20, 0))
        self.gui.restart_button.pack_forget()

        for button in self.gui.option_buttons:
            button.pack(anchor="w", padx=20, pady=5)

        self.gui.submit_button.pack(side="left", padx=10)
        self.gui.result_label.configure(text="")
        self.display_question()

    def determine_quiz_winner(self):
        if self.gui.score_player1 > self.gui.score_player2:
            self.gui.winner_label.configure(text=f"{self.gui.player1_name} is the winner!", text_color="green")
            self.gui.winner_label.pack(pady=(20, 0))
            print(f"{self.gui.player1_name} is the winner!")
        elif self.gui.score_player1 < self.gui.score_player2:
            self.gui.winner_label.configure(text="Player 2 is the winner!", text_color="green")
            self.gui.winner_label.pack(pady=(20, 0))
            print("Player 2 is the winner!")
        else:
            self.gui.winner_label.configure(text="It's a tie! Both players are winners!", text_color="green")
            self.gui.winner_label.pack(pady=(20, 0))
            print("It's a tie! Both players are winners!")

