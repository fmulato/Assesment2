import customtkinter as ctk
import quiz_logic as ql
from utils import select_random_elements

SIZE_WIDTH = 800
SIZE_HEIGHT = 600

class StartScreen:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Brain Up! - Registration")
        self.root.geometry(f"{SIZE_WIDTH}x{SIZE_HEIGHT}")

        font_instrcution = ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Instructions
        ctk.CTkLabel(self.root, text="Please enter your information:", font=font_instrcution, text_color='blue').grid(row=1, column=0, columnspan=4, padx=5, pady=5)


        # Player 1
        ctk.CTkLabel(self.root, text="Player 1 Nickname:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.player1_nickname = ctk.CTkEntry(self.root)
        self.player1_nickname.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.root, text="Player 1 Age:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.player1_age = ctk.CTkEntry(self.root, width=50)  # Reduzi a largura
        self.player1_age.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Player 2
        ctk.CTkLabel(self.root, text="Player 2 Nickname:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.player2_nickname = ctk.CTkEntry(self.root)
        self.player2_nickname.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.root, text="Player 2 Age:").grid(row=4, column=2, padx=5, pady=5, sticky="e")
        self.player2_age = ctk.CTkEntry(self.root, width=50)  # Reduzi a largura
        self.player2_age.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        # Button to start the game
        self.start_button = ctk.CTkButton(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=6, column=0, columnspan=4, pady=20)  # Espalha por todas as colunas

        # Configure column weights to make the layout responsive
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

        self.root.mainloop()  # Start the main loop

    def start_game(self):
        # Armazena os valores nos atributos da instância
        player1 = self.player1_nickname.get()
        age1 = self.player1_age.get()
        player2 = self.player2_nickname.get()
        age2 = self.player2_age.get()


        # Open the game window and start the game
        new_root = ctk.CTk()
        game = Gui(new_root, self, player1, player2)

        # Close the start screen
        self.root.destroy()

        game.run()

class Gui:
    def __init__(self, root, start_screen=None, player1='Player 1', player2='Player 2'):
        # Creation of the main window
        self.root = root  # Usa a nova janela criada
        self.root.title("Brain Up! Quiz Game")

        # Initial configuration of CustomTkinter
        ctk.set_appearance_mode("System")  # Appearance mode (System, Light, Dark)
        ctk.set_default_color_theme("blue")  # Default theme

        # Force the main window to appear centered on the screen
        screen_width = self.root.winfo_screenwidth()  # Get the screen's total width
        screen_height = self.root.winfo_screenheight()  # Get the screen's total height

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (SIZE_WIDTH // 2)  # Horizontal centering calculation
        y = (screen_height // 2) - (SIZE_HEIGHT // 2)  # Vertical centering calculation

        # Set the geometry of the window (width x height + position_x + position_y)
        self.root.geometry(f"{SIZE_WIDTH}x{SIZE_HEIGHT}+{x}+{y}")

        self.root.minsize(SIZE_WIDTH, SIZE_HEIGHT)  # Set the minimum size of the window
        self.root.maxsize(1.2 * SIZE_WIDTH, 1.2 * SIZE_HEIGHT)  # Set the maximum size of the window

        self.logic = ql.Logic(self)

        # Fonts
        font_player = ctk.CTkFont(family="Arial", size=18, weight="bold")
        font_score = ctk.CTkFont(family="Arial", size=16, weight="normal")
        font_quest = ctk.CTkFont(family="Arial", size=18, weight="bold")
        font_categ = ctk.CTkFont(family="Arial", size=20, weight="bold")

        # Left frame (20% of the width)
        self.frame_left = ctk.CTkFrame(self.root, width=int(0.2 * SIZE_WIDTH), height=SIZE_HEIGHT, fg_color="gray80")
        self.frame_left.grid(row=0, column=0, sticky="nsew")

        # Right frame (20% of the width)
        self.frame_right = ctk.CTkFrame(self.root, width=int(0.2 * SIZE_WIDTH), height=SIZE_HEIGHT, fg_color="gray80")
        self.frame_right.grid(row=0, column=2, sticky="nsew")

        # Central frame (60% of the width)
        self.frame_center = ctk.CTkFrame(self.root, width=int(0.6 * SIZE_WIDTH), height=SIZE_HEIGHT, fg_color="gray70")
        self.frame_center.grid(row=0, column=1, sticky="nsew")

        # Division of the central frame into three parts
        # Top frame (20% of the height)
        self.frame_center_top = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH), height=int(0.2 * SIZE_HEIGHT), fg_color="gray65")
        self.frame_center_top.grid(row=0, column=0, sticky="nsew")

        # Middle frame (60% of the height)
        self.frame_center_middle = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH), height=int(0.6 * SIZE_HEIGHT), fg_color="gray73")
        self.frame_center_middle.grid(row=1, column=0, sticky="nsew")

        # Bottom frame (20% of the height)
        self.frame_center_bottom = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH), height=int(0.2 * SIZE_HEIGHT), fg_color="gray65")
        self.frame_center_bottom.grid(row=2, column=0, sticky="nsew")

        # Configuration of proportions for the grids
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)  # Left frame
        self.root.grid_columnconfigure(1, weight=3)  # Central frame
        self.root.grid_columnconfigure(2, weight=1)  # Right frame

        self.frame_center.grid_rowconfigure(0, weight=1)  # Top frame
        self.frame_center.grid_rowconfigure(1, weight=3)  # Middle frame
        self.frame_center.grid_rowconfigure(2, weight=1)  # Bottom frame
        self.frame_center.grid_columnconfigure(0, weight=1)

        # Player 1
        self.player1 = player1
        self.player1_age = ""
        self.player1_id = ""
        self.timestamp1 = ""
        self.player1_label = ctk.CTkLabel(self.frame_left, text=f"   Player 1: {self.player1}   ",
                                          font=font_player)
        self.player1_label.pack(pady=10)
        self.score_player1 = 0
        self.score_player1_label = ctk.CTkLabel(self.frame_left, text=f"   Score: {self.score_player1}   ",
                                                font=font_score)
        self.score_player1_label.pack(pady=5)

        # Player 2
        self.player2 = player2
        self.player2_age = ""
        self.player2_id = ""
        self.timestamp2 = ""
        self.player2_label = ctk.CTkLabel(self.frame_right, text=f"   Player 2: {self.player2}   ",
                                          font=font_player)
        self.player2_label.pack(pady=10)
        self.score_player2 = 0
        self.score_player2_label = ctk.CTkLabel(self.frame_right, text=f"   Score: {self.score_player2}   ",
                                                font=font_score)
        self.score_player2_label.pack(pady=5)

        # Questions
        self.category_label = ctk.CTkLabel(self.frame_center_top, text="Category:", font=font_categ, text_color='blue')
        self.category_label.pack(pady=5)
        self.question_label = ctk.CTkLabel(
            self.frame_center_top, text="Question will appear here", font=font_quest, wraplength=500
        )
        self.question_label.pack(pady=20)

        # Results
        self.winner_label = ctk.CTkLabel(self.frame_center_middle, text="Winner:", font=font_categ, text_color='green')

        self.result_label = ctk.CTkLabel(self.frame_center_middle, text="", font=("Arial", 16), text_color="black")
        self.result_label.pack(pady=10)

        # Load questions
        #self.logic.save_player_info()
        #self.questions = self.logic.load_questions("questions.json")
        #self.selected_questions = select_random_elements(self.questions)
        self.current_question_index = 0
        #self.logic.display_question()

        # Frame for buttons
        self.frame_center_bottom.grid_columnconfigure(0, weight=1)
        self.frame_center_bottom.grid_columnconfigure(1, weight=1)
        self.frame_center_bottom.grid_columnconfigure(2, weight=1)
        self.submit_button = ctk.CTkButton(self.frame_center_bottom, text="Submit", command=self.logic.check_answer, font=("Arial", 14), width=100)
        self.submit_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.next_button = ctk.CTkButton(self.frame_center_bottom, text="Next", command=self.logic.next_question, font=("Arial", 14), width=100)
        self.next_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        #self.next_button.grid_forget()
        self.restart_button = ctk.CTkButton(self.frame_center_bottom, text="Restart Quiz", command=self.logic.restart_quiz, font=("Arial", 14), width=100)
        self.restart_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        #self.restart_button.grid_forget()

    def run(self):
        self.root.mainloop()
