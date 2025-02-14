import customtkinter as ctk
import quiz_logic as ql
import random

# Import required for selecting random questions
SIZE_WIDTH = 800
SIZE_HEIGHT = 600

class Gui:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Game for Kids")
        master.geometry(f"{SIZE_WIDTH}x{SIZE_HEIGHT}")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.logic = ql.Logic(self)

        # Frames
        self.frame_left = ctk.CTkFrame(master, width=0.25 * SIZE_WIDTH)
        self.frame_center = ctk.CTkFrame(master, width=0.50 * SIZE_WIDTH)
        self.frame_right = ctk.CTkFrame(master, width=0.25 * SIZE_WIDTH)
        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_center.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.frame_right.pack(side="left", fill="y", padx=10, pady=10)

        # Fonts
        font_player = ctk.CTkFont(family="Arial", size=18, weight="bold")
        font_score = ctk.CTkFont(family="Arial", size=16, weight="normal")
        font_quest = ctk.CTkFont(family="Arial", size=18, weight="bold")
        font_categ = ctk.CTkFont(family="Arial", size=20, weight="bold")

        # Player 1
        self.player1_label = ctk.CTkLabel(self.frame_left, text="        Player 1:       ", font=font_player)
        self.player1_label.pack(pady=10)
        self.score_player1 = 0
        self.score_player1_label = ctk.CTkLabel(self.frame_left, text=f"Score: {self.score_player1}", font=font_score)
        self.score_player1_label.pack(pady=5)

        # Player 2
        self.player2_label = ctk.CTkLabel(self.frame_right, text="        Player 2:       ", font=font_player)
        self.player2_label.pack(pady=10)
        self.score_player2 = 0
        self.score_player2_label = ctk.CTkLabel(self.frame_right, text=f"Score: {self.score_player2}", font=font_score)
        self.score_player2_label.pack(pady=5)

        # Questions
        self.category_label = ctk.CTkLabel(self.frame_center, text="Category: ", font=font_categ, text_color='blue')
        self.category_label.pack(pady=5)
        self.question_label = ctk.CTkLabel(
            self.frame_center, text="Question will appear here", font=font_quest, wraplength=500
        )
        self.question_label.pack(pady=20)

        # Options
        self.options_var = ctk.StringVar()
        self.option_buttons = []
        for i in range(4):
            option_button = ctk.CTkRadioButton(
                self.frame_center,
                text=f"Option {i + 1}",
                variable=self.options_var,
                value=str(i + 1),
                font=("Arial", 14),
            )
            option_button.pack(anchor="w", padx=20, pady=5)
            self.option_buttons.append(option_button)

        # Frame for Submit and Next buttons
        self.button_frame = ctk.CTkFrame(self.frame_center)
        self.button_frame.pack(pady=20, fill="x")  # Fixed position below the options
        self.submit_button = ctk.CTkButton(
            self.button_frame, text="Submit", command=self.logic.check_answer, font=("Arial", 14), width=100
        )
        self.submit_button.pack(side="top", anchor='center', padx=10)
        self.next_button = ctk.CTkButton(
            self.button_frame, text="Next", command=self.logic.next_question, font=("Arial", 14), width=100
        )
        self.next_button.pack(side="top", anchor='center', padx=10)
        self.next_button.pack_forget()  # Hide the Next button initially

        # Label to display "Correct" or "Incorrect"
        self.result_label = ctk.CTkLabel(self.frame_center, text="", font=("Arial", 16), text_color="black")
        self.result_label.pack(pady=10)

        # Restart button
        self.restart_button = ctk.CTkButton(
            self.frame_center, text="Restart Quiz", command=self.logic.restart_quiz, font=("Arial", 14)
        )
        self.restart_button.pack(pady=20)
        self.restart_button.pack_forget()  # Hide the restart button initially

        # Load questions and select three random ones
        self.questions = self.logic.load_questions("questions.json")
        self.selected_questions = random.sample(list(enumerate(self.questions, start=1)), 3)  # Select 3 random questions
        self.current_question_index = 0
        self.logic.display_question()


