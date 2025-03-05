"""
This module contains the logic for the quiz game. It manages the display of questions, options, and results.
It provides the following functionality:
1. Display question: Displays the current question and options on the screen.
2. Display result: Displays the result of the current question (correct or incorrect).
3. Determine quiz winner: Determines the winner of the quiz based on the scores of the players.
4. Next turn: Moves to the next player's turn.
5. Check answer: Checks the selected answer and updates the score accordingly.
6. Start timer: Starts the countdown timer for each question.
7. Stop timer: Stops the countdown timer.
8. Next question: Moves to the next question in the quiz.
9. Underline current player: Highlights the current player in the GUI.
"""
import time
import pygame
from utils import Utils
import gui



class Logic():
    def __init__(self, gs):
        self.gs = gs
        self.current_player = 1  # 1 for Player 1, 2 for Player 2
        self.time_limit = gui.LIMIT_TIME
        self.timer_active = False    # To track if the timer is running
        self.underline_current_player()

    def start_timer(self):
        self.timer_active = True
        self.gs.countdown(self.time_limit)

    def stop_timer(self):
        self.timer_active = False

    def display_question(self):
        # Check if there are more questions available to display
        if self.gs.current_question_index < len(self.gs.selected_questions):
            self.gs.countdown(self.time_limit)  # Start the timer

        # Disable the next button and submit button
        self.gs.next_button.configure(state="disabled")
        self.gs.submit_button.configure(state="disabled")

        if self.gs.current_question_index < len(self.gs.selected_questions):
            self.gs.question_number, self.gs.question_data = self.gs.selected_questions[self.gs.current_question_index]
            is_last_round = self.is_last_round()  # Check if it's the last round

            # Update category label with warning if it's the last question
            if is_last_round:
                self.gs.category_label.configure(text=f"Category: {self.gs.question_data[1]} (Last Question!)")
                self.play_last_question_sound()  # Play sound for last question
            else:
                self.gs.category_label.configure(text=f"Category: {self.gs.question_data[1]}")

            self.gs.question_label.configure(text=f"{self.gs.current_question_index + 1}. {self.gs.question_data[2]}")

            # Extract options and shuffle them
            options = self.gs.question_data[3:7]
            correct_answer = self.gs.question_data[7]

            # Shuffle answers using Utils
            utils = Utils()
            shuffled_options, new_correct_answer, index_mapping = utils.shuffle_answers(options, correct_answer)
            self.gs.index_mapping = index_mapping  # store the index mapping for later use

            for i, option in enumerate(shuffled_options):
                self.gs.option_buttons[i].configure(text=option, text_color="black")
                self.gs.option_buttons[i]._value = str(i + 1)

            # Update the correct answer index in question data
            self.gs.question_data = list(self.gs.question_data)  # Convert tuple to list
            self.gs.question_data[7] = new_correct_answer  # Update correct answer position

            self.gs.options_var.set(None)
            self.gs.result_label.configure(text="")
            self.gs.winner_label.grid_forget()

        else:  # No more questions available
            self.gs.question_label.configure(text="No more questions!")
            self.gs.restart_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

            # Stop the timer and sounds
            self.stop_timer()
            self.gs.tic_tac_sound.stop()
            self.gs.buzz_sound.stop()

            self.determine_quiz_winner()

            for button in self.gs.option_buttons:
                button.grid_forget()
            self.gs.submit_button.grid_forget()
            self.gs.result_label.configure(text="")
            self.gs.result_label.grid_forget()
            self.gs.next_button.forget()

        # Update the turn label
        for i, button in enumerate(self.gs.option_buttons):
            button.configure(command=lambda i=i: self.gs.enable_submit_button(i))

    def play_last_question_sound(self):
        """Play sound to indicate it's the last question."""
        self.last_question_sound = pygame.mixer.Sound("bonus.mp3")

        self.last_question_sound.play()

        # Show the last question dialog
        gui.LastQuestionDialog(self.gs.root, self.gs.player1, self.gs.player2, self.current_player)

        time.sleep(0.2)

    def next_turn(self):
        """Move to the next player's turn."""

        if self.gs.current_question_index < len(self.gs.selected_questions):
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1

            self.gs.result_label.configure(text="")  # Clear previous result
            self.gs.options_var.set(None)  # Reset selected option
            if self.last_question == False:
                self.start_timer() # Start timer for the next player
            if self.last_question == True:
                self.stop_timer()
                self.gs.tic_tac_sound.stop()
                self.gs.buzz_sound.stop()

            self.underline_current_player()

        else:
            self.gs.turn_label.configure(text="")  # Clear turn label

    def is_last_round(self):
        """Check if the current question is one of the last two questions."""
        return self.gs.current_question_index >= len(self.gs.selected_questions) - 2

    def check_answer(self):
        """Check the selected answer."""
        # Stop the timer and sounds
        self.stop_timer()
        self.gs.tic_tac_sound.stop()
        self.gs.buzz_sound.stop()

        # Ensure the timer label is not displayed
        if hasattr(self.gs, "timer") and self.gs.timer:
            self.gs.timer.grid_forget()

        # Get the selected option
        selected_option = self.gs.options_var.get()
        _, question_data = self.gs.selected_questions[self.gs.current_question_index]
        correct_answer = question_data[7]

        # Check if the answer is given within the time limit
        if selected_option is None or selected_option == 'None':
            self.next_turn()  # Move to the next player's turn
            return

        # Try to convert selected_option to an integer
        try:
            selected_option_int = int(selected_option)
        except ValueError:
            self.gs.result_label.configure(text="Invalid selection!", text_color="red")
            self.next_turn()  # Move to the next player's turn
            return

        for button in self.gs.option_buttons:
            button.configure(text_color="black")

        # Determine if it's the last round
        is_last_round = self.is_last_round()

        # Check if the selected answer is correct
        if selected_option_int == self.gs.index_mapping[correct_answer]:
            self.gs.result_label.configure(text="Correct!", text_color="blue")

            # Update the score for the current player
            points = 20 if is_last_round else 10  # Double points for the last question
            if self.current_player == 1:
                self.gs.score_player1 += points
                self.gs.score_player1_label.configure(text=f"Score: {self.gs.score_player1}")
            else:
                self.gs.score_player2 += points
                self.gs.score_player2_label.configure(text=f"Score: {self.gs.score_player2}")

            self.gs.option_buttons[self.gs.index_mapping[correct_answer] - 1].configure(text_color="blue")
        else:
            self.gs.result_label.configure(text="Incorrect!", text_color="red")
            # Deduct points for wrong answer only if was last question
            penalty = -10 if is_last_round else 0
            if self.current_player == 1:
                if self.gs.score_player1 > 0: # only deduct if player 1 has points
                    self.gs.score_player1 += penalty  # Deduct 10 points for wrong answer
                    self.gs.score_player1_label.configure(text=f"Score: {self.gs.score_player1}")
            else:
                if self.gs.score_player2 > 0:  # only deduct if player 2 has points
                    self.gs.score_player2 += penalty  # Deduct 10 points for wrong answer
                    self.gs.score_player2_label.configure(text=f"Score: {self.gs.score_player2}")

            self.gs.option_buttons[self.gs.index_mapping[correct_answer] - 1].configure(text_color="blue")
            if selected_option:
                self.gs.option_buttons[selected_option_int - 1].configure(text_color="red")

        # Enable the next button and disable the submit button
        self.gs.submit_button.configure(state="disabled")
        self.gs.next_button.configure(state="normal")

        # check if the timer is active before playing the sound
        if self.timer_active:
            self.gs.submit_button.configure(state="disabled")
            self.gs.next_button.configure(state="normal")

    def next_question(self):
        """Move to the next question."""
        # check if there are more questions available to display
        self.last_question = False
        if self.gs.current_question_index < len(self.gs.selected_questions):
            self.gs.current_question_index += 1
            self.gs.submit_button.configure(state="normal")
            self.gs.next_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            self.display_question()
            self.next_turn()
        else:
            self.last_question = True
            self.stop_timer()
            self.gs.tic_tac_sound.stop()
            self.gs.buzz_sound.stop()
            self.gs.timer.grid_forget()
            self.determine_quiz_winner()
            self.next_turn()


    def determine_quiz_winner(self):
        self.stop_timer()
        self.gs.timer.grid_forget()

        # Play the winner sound
        if not hasattr(self, 'winner_sound_played'):
            self.tic_tac_sound = pygame.mixer.Sound("winner.wav")
            self.tic_tac_sound.play()
            self.winner_sound_played = True  # set the flag to True

        if self.gs.score_player1 > self.gs.score_player2:
            self.gs.winner_label.configure(text=f"{self.gs.player1} ({self.gs.age1}) is the winner!", text_color="green")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print(f"{self.gs.player1_label} is the winner!")
            self.gs.next_button.grid_forget()

        elif self.gs.score_player1 < self.gs.score_player2:
            self.gs.winner_label.configure(text=f"{self.gs.player2} ({self.gs.age2}) is the winner!", text_color="blue")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print("Player 2 is the winner!")
            self.gs.next_button.grid_forget()

        else:
            self.gs.winner_label.configure(text="It's a tie! Both players are winners!", text_color="green")
            self.gs.winner_label.grid(padx=20, pady=(20, 0), sticky="nsew")
            print("It's a tie! Both players are winners!")
            self.gs.next_button.grid_forget()

    def underline_current_player(self):
        if self.current_player == 1:
            self.gs.player1_label.configure(font=("Arial", 14, "bold"), fg_color="white", padx=7, pady=7)
            self.gs.player2_label.configure(font=("Arial", 14), fg_color="gray80")
        else:
            self.gs.player2_label.configure(font=("Arial", 14, "bold"), fg_color="white", padx=7, pady=7)
            self.gs.player1_label.configure(font=("Arial", 14), fg_color="gray80")

    def hint(self):
        pass

    def skip(self):
        pass

