import customtkinter as ctk
import quiz_logic as ql
from utils import select_random_elements

SIZE_WIDTH = 800
SIZE_HEIGHT = 600

class Gui:
    def __init__(self):

        # Initial configuration of CustomTkinter
        ctk.set_appearance_mode("System")  # Appearance mode (System, Light, Dark)
        ctk.set_default_color_theme("blue")  # Default theme

        # Creation of the main window
        self.root = ctk.CTk()
        self.root.title("Brain up! Quiz Game for Kids")

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
        self.player1_name = "Player 1"
        self.player1_age = ""
        self.player1_id = ""
        self.timestamp1 = ""
        self.player1_label = ctk.CTkLabel(self.frame_left, text=f"   Player 1: {self.player1_name}   ",
                                          font=font_player)
        self.player1_label.pack(pady=10)
        self.score_player1 = 0
        self.score_player1_label = ctk.CTkLabel(self.frame_left, text=f"   Score: {self.score_player1}   ",
                                                font=font_score)
        self.score_player1_label.pack(pady=5)

        # Player 2
        self.player2_name = "Player 2"
        self.player2_age = ""
        self.player2_id = ""
        self.timestamp2 = ""
        self.player2_label = ctk.CTkLabel(self.frame_right, text=f"   Player 2: {self.player2_name}   ",
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
        self.winner_label = ctk.CTkLabel(self.frame_center_top, text="Winner:", font=font_categ, text_color='green')

    def run(self):
        self.root.mainloop()
