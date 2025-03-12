"""
This module contains the main GUI classes for the Brain Up! quiz game.

Classes:
- StartScreen: The first window where players are selected. Manages player registration, setups and starts the game.
- GameScreen: The main game window where the quiz is played. Manages the display of questions, options, and results.

"""

import datetime
import sys
import tkinter.filedialog as filedialog
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import pygame
import quiz_logic as ql
from database_management import DataBase
from utils import CustomPopup, Utils, SIZE_WIDTH, SIZE_HEIGHT

class RootUtils:
    """Utility class for centering the main window on the screen."""
    @staticmethod
    def center_window(root, width, height):
        """Center the main window on the screen."""
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(width, height)
        root.maxsize(width, height)

class StartScreen:
    """The first window where players are selected. Manages player registration, setups and starts the game."""
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Brain Up! - Registration")
        # Add user management instance
        self.db_manager = DataBase()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Selected players list (Max 2 people)
        self.selected_players = []

        # Force the main window to appear centered on the screen
        RootUtils.center_window(self.root, SIZE_WIDTH, SIZE_HEIGHT)

        self.player1 = "Player 1"
        self.age1 = ""
        self.player2 = "Player 2"
        self.age2 = ""

        font_instruction = ctk.CTkFont(family="Arial", size=16, weight="bold")

        # configure the grid
        self.root.grid_columnconfigure(0, weight=1)

        # Frame to label
        label_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        label_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        label_frame.grid_columnconfigure(0, weight=1)

        # Configure columns to have equal weight for balanced spacing
        label_frame.columnconfigure(0, weight=1)  # Column for Player 1
        label_frame.columnconfigure(1, weight=1)  # Column for "VS"
        label_frame.columnconfigure(2, weight=1)  # Column for Player 2

        self.label_instructions = ctk.CTkLabel(label_frame, text="Please select players:", font=font_instruction,
                     text_color='blue')
        self.label_instructions.grid(row=0, column=1, pady=10)

        # Player 1:
        self.label_player1 = ctk.CTkLabel(label_frame, text=f"Player 1 (age):", font=font_instruction, text_color='green')
        self.label_player1.grid(row=1, column=0, pady=5, sticky="ew")
        self.label_player1_name = ctk.CTkLabel(label_frame, text="", font=font_instruction, text_color='green')
        self.label_player1_name.grid(row=2, column=0, pady=5, sticky="ew")
        #self.label_player1_age = ctk.CTkLabel(label_frame, text=self.age1, font=font_instruction, text_color='green')
        #self.label_player1_age.grid(row=2, column=1, pady=5, sticky="ew")

        # versus
        self.label_vs = ctk.CTkLabel(label_frame, text="      VS      ", font=font_instruction, text_color='black')
        self.label_vs.grid(row=1, column=1, pady=5, sticky="ew")

        # Player 2:
        self.label_player2 = ctk.CTkLabel(label_frame, text="Player 2 (age):", font=font_instruction, text_color='blue')
        self.label_player2.grid(row=1, column=2, pady=5, sticky="ew")
        self.label_player2_name = ctk.CTkLabel(label_frame, text="", font=font_instruction, text_color='blue')  # Label para o nome do jogador 2
        self.label_player2_name.grid(row=2, column=2, pady=5, sticky="ew")

        # Frame for player buttons
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        # Fetch & display players from database
        self.display_player_buttons()

        # Button to start the game (Initially disabled)
        self.start_button = ctk.CTkButton(self.root, text="Start Game", command=self.start_game, font=("Arial", 14),
                                          width=100, state="normal")
        self.start_button.grid(row=2, column=0, pady=10)

        self.lower_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.lower_frame.grid(row=5, column=0, pady=10, sticky="ew")
        self.lower_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Equal spacing for 3 columns

        # Add delete_name_button
        self.delete_name_button = ctk.CTkButton(self.lower_frame, text="Delete Player", command=self.delete_player, font=("Arial", 14), width=100, state="normal")
        self.delete_name_button.grid(row=4, column=0, padx=10, pady=10)

        # Add New Name button
        self.add_name_button = ctk.CTkButton(self.lower_frame, text="Add New Name", command=self.add_new_name, font=("Arial", 14), width=100, state="normal")
        self.add_name_button.grid(row=4, column=1, padx=10, pady=10)

        # Add update_questions button
        self.update_questions_button = ctk.CTkButton(self.lower_frame, text="Update Questions", command=self.update_new_questions, font=("Arial", 14), width=100, state="normal")
        self.update_questions_button.grid(row=4, column=2, padx=10, pady=10)

        # Add show_rules_button
        self.show_rules_button = ctk.CTkButton(self.lower_frame, text="Show Rules", command=self.show_rules, font=("Arial", 14), width=100, state="normal")
        self.show_rules_button.grid(row=5, column=0, padx=10, pady=10)

        # Add setup_button
        self.setup_button = ctk.CTkButton(self.lower_frame, text="Setup", command=self.open_setup, font=("Arial", 14), width=100, state="normal")
        self.setup_button.grid(row=5, column=1, padx=10, pady=10)

        # Add ranking_button
        self.ranking_button = ctk.CTkButton(self.lower_frame, text="Show Ranking", command=self.show_ranking, font=("Arial", 14), width=100, state="normal")
        self.ranking_button.grid(row=5, column=2, padx=10, pady=10)

        self.exit_button = ctk.CTkButton(self.lower_frame, text="Exit", command=self.exit, font=("Arial", 14), width=100)
        self.exit_button.grid(row=6, column=1, padx=10, pady=10)

        self.root.mainloop()

    def exit(self):
        """ Exits the game. """
        sys.exit()

    # def update_questions(self):
    #     """Reload questions.json and update the database."""
    #     db = DataBase()
    #     db.load_db_from_json("questions.json")  # Load questions from JSON
    #     CustomPopup("Success", "Questions database has been updated!")

    def update_new_questions(self):
        """Open a file dialog to choose a JSON file and update the questions."""

        msg = CTkMessagebox(title="Instructions",
                      message="Choose a JSON file to load new categories and questions.",
                      icon="info",
                      option_1="OK")
        response1 = msg.get()

        if response1 == "OK":
            json_file = filedialog.askopenfilename(
                                                    title="Select file",
                                                    filetypes=[("JSON Files", "*.json")],
                                                    defaultextension=".json"
                                                    )
        else:
            return

        if json_file:
            msg = CTkMessagebox(title="Confirm",
                                message="Do you want to update the database with this file?",
                                icon="question",
                                option_1="No",
                                option_2="Yes")
            response = msg.get()

            if response == "Yes":
                db = DataBase()
                db.load_db_from_json(json_file)
                CTkMessagebox(message="The database has been updated!", icon="check", option_1="OK")
            elif response == "No":
                print("Operation canceled.")


    def display_player_buttons(self):
        """Display player buttons."""
        # Clear the button frame, before adding new buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        players = self.db_manager.get_all_players()

        if not players:
            ctk.CTkLabel(self.button_frame, text="No players found. Add players first!", font=("Arial", 14)).grid(row=0, column=0, pady=5, sticky="nesw")
            return

        # Variables to keep track of row and column
        row = 0
        col = 0
        max_columns = 6

        for username, age in players:
            btn = ctk.CTkButton(
                self.button_frame,
                text=f"{username} ({age})",
                command=lambda u=username, a=age: self.toggle_player_selection(u, a, btn),
                width=120
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nesw")

            col += 1
            if col > max_columns:  # Go to next row
                col = 0
                row += 1

        # Configuration for the grid
        for i in range(max_columns):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def toggle_player_selection(self, username, age, button):
        """Handles selecting players, enforcing a maximum of two at a time,
        and rotating selection when a third is picked."""

        player = (username, age)

        if player in self.selected_players:
            self.selected_players.remove(player)
        else:
            if len(self.selected_players) == 2:
                self.selected_players.pop(0)  # Exclude

            self.selected_players.append(player)

        # Update button colors and start button
        self.update_button_colors()
        self.update_start_button()

        # Update player names
        if len(self.selected_players) == 1:
            self.label_player1_name.configure(text=f"{self.selected_players[0][0]} ({self.selected_players[0][1]})")
            self.label_player2_name.configure(text="")
        elif len(self.selected_players) == 2:
            self.label_player1_name.configure(text=f"{self.selected_players[0][0]} ({self.selected_players[0][1]})")
            self.label_player2_name.configure(text=f"{self.selected_players[1][0]} ({self.selected_players[1][1]})")
        else:
            self.label_player1_name.configure(text="")
            self.label_player2_name.configure(text="")

    def update_button_colors(self):
        """Update the colors of the player buttons based on selection.
        Green for player 1, Blue for player 2."""

        for btn in self.button_frame.winfo_children():
            btn.configure(fg_color="lightgray", state="normal")  # Grant all buttons the "normal" state

        for index, (username, age) in enumerate(self.selected_players):
            for btn in self.button_frame.winfo_children():
                if username in btn.cget("text"):  # Verify if name is in the button
                    btn.configure(fg_color="green" if index == 0 else "blue", state="normal")
                    break

    def update_start_button(self):
        """Enables the start button when 2 players are selected"""
        self.start_button.configure(state="normal" if len(self.selected_players) == 2 else "disabled")

        if len(self.selected_players) == 2:
            self.player1, self.age1 = self.selected_players[0]
            self.player2, self.age2 = self.selected_players[1]

            # Update player names
            self.label_player1_name.configure(text=self.player1)
            self.label_player2_name.configure(text=self.player2)
        elif len(self.selected_players) == 1:
            self.player1, self.age1 = self.selected_players[0]
            self.player2, self.age2 = "", ""

            self.label_player1_name.configure(text=self.player1)
            self.label_player2_name.configure(text="")
        else:
            self.player1, self.age1 = "", ""
            self.player2, self.age2 = "", ""

            self.label_player1_name.configure(text="")
            self.label_player2_name.configure(text="")

    def add_new_name(self):
        """Open the Add Name dialog."""
        AddNameDialog(self.root, self.db_manager, self)

    def delete_player(self):
        """Delete the selected player from the database and refresh the player list."""
        if not self.selected_players:
            CustomPopup("Warning", "Please select a player to delete.")
            return

        player_to_delete = self.selected_players[0]  # Delete the first selected player
        username_to_delete = player_to_delete[0]  # Extract username

        # Confirmation popup
        msg = CTkMessagebox(
            title="Confirm Deletion",
            message=f"Are you sure you want to delete {username_to_delete}?",
            icon="question",
            option_1="No",
            option_2="Yes"
        )
        response = msg.get()

        if response == "Yes":
            db = DataBase()
            deletion_success = db.delete_player(username_to_delete)  # Pass username to DB method

            if deletion_success:
                CustomPopup("Success", f"Player {username_to_delete} has been deleted.")
            else:
                CustomPopup("Error", f"Failed to delete player {username_to_delete}.")

            # Refresh the player list on the screen
            self.selected_players.clear()  # Clear selection
            self.display_player_buttons()  # Refresh player buttons

    def show_ranking(self):
        """ Open the Show Ranking dialog. """
        ShowRankingDialog(self.root, self.db_manager)

    def show_rules(self):
        """ Open the Show Rules dialog. """
        ShowRulesDialog(self.root)

    def open_setup(self):
        """ Open the Setup dialog. """
        SetupDialog(self.root)

    def start_game(self):
        """ Start the game with selected players. """
        if len(self.selected_players) != 2:
            CustomPopup("Warning!", "Select two players to start the game.")
            return  # Ensure exactly two players are selected

        # Check if questions exist in the database
        from database_management import DataBase
        db = DataBase()
        questions = db.load_questions()
        if not questions:  # If no questions are found
            CustomPopup("Error!", "No questions are available. Please load questions from 'questions.json'.")
            return


        player1, age1 = self.selected_players[0]
        player2, age2 = self.selected_players[1]

        print(f"Starting game with: {player1} ({age1}) vs {player2} ({age2})")

        # Hide current screen
        self.root.withdraw()

        # Open the game window (Assuming you have a game class)
        game_window = ctk.CTk()
        game = GameScreen(game_window, player1, age1, player2, age2)
        game.run()

class AddNameDialog(ctk.CTkToplevel):
    """ Custom pop-up window for entering Name and Date of Birth using only customtkinter. """
    def __init__(self, parent, db_manager, start_screen):
        super().__init__(parent)  # Using parent (self.root) for CTkToplevel
        self.db_manager = db_manager
        self.start_screen = start_screen  # Reference to instance
        self.parent = parent
        self.result = None

        self.title("Add New Player")

        window_width = 290
        window_height = 140
        RootUtils.center_window(self, window_width, window_height)

        self.grab_set()  # Make the window modal (force user interaction)

        # Configure grid for proper alignment
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)  # Column for entry fields
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Label and Entry for Name
        ctk.CTkLabel(self, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(self, width=150)  # Fixed width for better control
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Label for Birthday
        ctk.CTkLabel(self, text="Select your Birthday:").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Combo box for Day
        self.days = [str(i).zfill(2) for i in range(1, 32)]  # 01, 02, ..., 31
        self.selected_day = ctk.StringVar(value=self.days[0])  # Default to 01
        self.day_menu = ctk.CTkOptionMenu(self, variable=self.selected_day, values=self.days, width=60)
        self.day_menu.grid(row=2, column=0, padx=(10, 0), pady=5, sticky="w")

        # Combo box for Month
        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.selected_month = ctk.StringVar(value=self.months[0])  # Default to January
        self.month_menu = ctk.CTkOptionMenu(self, variable=self.selected_month, values=self.months, width=100)
        self.month_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Combo box for Year
        current_year = datetime.datetime.now().year
        self.years = [str(year) for year in range(current_year - 15, current_year - 8)]
        self.selected_year = ctk.StringVar(value=self.years[0])
        self.year_menu = ctk.CTkOptionMenu(self, variable=self.selected_year, values=self.years, width=60)
        self.year_menu.grid(row=2, column=1, padx=(110, 0), pady=5, sticky="w")

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text="OK", command=self.apply, width=100)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)
        #self.submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def save_birthday(self):
        """ Save the selected birthday as a string in the format "YYYY-MM-DD" """
        birthday_entry = f"{self.selected_year.get()}-{self.months.index(self.selected_month.get()) + 1:02}-{self.selected_day.get()}"
        return birthday_entry

    def apply(self):
        """ Save input values when OK is pressed """
        name = self.name_entry.get()
        birthday = self.save_birthday()

        if not name or not birthday:
            CustomPopup("Warning", "Both fields are required.")
            return

        success = self.db_manager.register_user(name, birthday)
        if success:
            self.start_screen.display_player_buttons()
            self.withdraw()  # Hide the pop-up after success

class GameScreen:
    """ Game Screen Class """

    def __init__(self, root, player1='Player 1', age1="", player2='Player 2', age2=""):
        # Create the main window
        self.root = root
        self.root.title("Brain Up! Quiz Game")

        self.player1 = player1
        self.age1 = age1
        self.player2 = player2
        self.age2 = age2

        self.seen_last_question = {} # dictionary to keep track of seen last questions

        pygame.mixer.init()

        # Code for the GameScreen class
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Force the main window to appear centered on the screen
        RootUtils.center_window(self.root, SIZE_WIDTH, SIZE_HEIGHT)

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
        self.frame_center_top = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH),
                                             height=int(0.2 * SIZE_HEIGHT), fg_color="gray65")
        self.frame_center_top.grid(row=0, column=0, sticky="nsew")

        # Middle frame (60% of the height)
        self.frame_center_middle = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH),
                                                height=int(0.6 * SIZE_HEIGHT), fg_color="gray73")
        self.frame_center_middle.grid(row=1, column=0, sticky="nsew")

        # Bottom frame (20% of the height)
        self.frame_center_bottom = ctk.CTkFrame(self.frame_center, width=int(0.6 * SIZE_WIDTH),
                                                height=int(0.2 * SIZE_HEIGHT), fg_color="gray65")
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

        bottom_spacer = ctk.CTkFrame(self.frame_left, height=70, fg_color="transparent")
        bottom_spacer.pack(side="bottom")

        self.skips_bal_player1 = 2
        self.skips_bal_player2 = 2

        # Player 1
        self.player1_label = ctk.CTkLabel(self.frame_left, text=f" Player 1 (age): \n\n {self.player1} ({self.age1})", font=font_player, text_color='green')
        self.player1_label.pack(pady=10)
        self.score_player1 = 0
        self.score_player1_label = ctk.CTkLabel(self.frame_left, text=f" Score: {self.score_player1} ", font=font_score)
        self.score_player1_label.pack(pady=5)

        self.hint_bal_player1 = 2


        # Hints and Skips balance
        self.hint_bal_player1_label = ctk.CTkLabel(self.frame_left, text=f" Hints left: {self.hint_bal_player1}", font=font_score, text_color="green")

        self.hint_bal_player1_label.pack(pady=5, side="bottom")
        self.skips_bal_player1_label = ctk.CTkLabel(self.frame_left, text=f" Skips left: {self.skips_bal_player1}", font=font_score, text_color="green")
        self.skips_bal_player1_label.pack(pady=5, side="bottom")
        self.skips_bal_player1_label.pack(pady=5, side="bottom")

        bottom_spacer = ctk.CTkFrame(self.frame_right, height=70, fg_color="transparent")
        bottom_spacer.pack(side="bottom")

        # Player 2
        self.player2_label = ctk.CTkLabel(self.frame_right, text=f" Player 2 (age):\n\n {self.player2} ({self.age2})", font=font_player, text_color='blue')
        self.player2_label.pack(pady=10)
        self.score_player2 = 0
        self.score_player2_label = ctk.CTkLabel(self.frame_right, text=f" Score: {self.score_player2} ", font=font_score)
        self.score_player2_label.pack(pady=5)

        self.hint_bal_player2 = 2

        # Hints and Skips balance
        self.hint_bal_player2_label = ctk.CTkLabel(self.frame_right, text=f" Hints left: {self.hint_bal_player2}", font=font_score, text_color="blue")

        self.hint_bal_player2_label.pack(pady=5, side="bottom")
        self.skips_bal_player2_label = ctk.CTkLabel(self.frame_right, text=f" Skips left: {self.skips_bal_player2}", font=font_score, text_color="blue")
        self.skips_bal_player2_label.pack(pady=5, side="bottom")

        # Questions
        # self.category_label = ctk.CTkLabel(self.frame_center_top, text="Category:", font=font_categ, text_color='blue')
        # self.category_label.grid(row=0, column=0, pady=10, padx=10)
        # self.question_label = ctk.CTkLabel(self.frame_center_top, text="Question will appear here", font=font_quest, wraplength=500)
        # self.question_label.grid(row=1, column=0, pady=10, padx=10)

        # Questions
        self.category_label = ctk.CTkLabel(self.frame_center_top, text="Category:", font=font_categ, text_color='blue')
        self.category_label.grid(row=0, column=0, pady=10, padx=10)

        self.question_label = ctk.CTkLabel(self.frame_center_top, text="Question will appear here", font=font_quest)
        self.question_label.grid(row=1, column=0, pady=10, padx=10)

        # Function to update wraplength - fit text according to frame
        def update_wraplength():
            frame_width = self.frame_center_top.winfo_width()
            self.question_label.configure(wraplength=int(frame_width * 0.8))

        # Call the function once to set the initial wraplength
        self.frame_center_top.bind("<Configure>", lambda e: update_wraplength())

        # Options
        self.options_var = ctk.StringVar()
        self.option_buttons = []
        for i in range(4):
            option_button = ctk.CTkRadioButton(
                self.frame_center_middle,
                text=f"Option {i + 1}",
                variable=self.options_var,
                value=str(i + 1),
                font=("Arial", 14),
            )
            option_button.grid(row=i, column=0, sticky="nsew", padx=10, pady=10)
            self.option_buttons.append(option_button)

        # Results
        self.winner_label = ctk.CTkLabel(self.frame_center_middle, text="Winner:", font=font_categ, text_color='green')
        self.result_label = ctk.CTkLabel(self.frame_center_middle, text="", font=("Arial", 16), text_color="black")
        self.result_label.grid(pady=10, padx=10, sticky="nsew", row=5, column=0)

        # Load questions
        self.questions = DataBase().load_questions()
        number_question = DataBase().update_global_settings()[1]
        self.selected_questions = Utils().select_random_elements(self.questions, number_question * 2)
        self.current_question_index = 0

        self.frame_center_bottom.grid_columnconfigure(0, weight=1)
        self.frame_center_bottom.grid_columnconfigure(1, weight=1)
        self.frame_center_bottom.grid_columnconfigure(2, weight=1)

        self.exit_button = ctk.CTkButton(self.frame_center_bottom, text="Exit", command=self.exit, font=("Arial", 14), width=100)
        self.exit_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # label to show the current player
        self.turn_label = ctk.CTkLabel(self.frame_center_bottom, text="", font=("Arial", 16), text_color="black")
        self.turn_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.timer = ctk.CTkLabel(self.frame_center_bottom, font=("Arial", 24))
        self.timer.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.timer.grid_forget()

        self.logic = ql.Logic(self)

        self.submit_button = ctk.CTkButton(self.frame_center_bottom, text="Submit", command=self.logic.check_answer, font=("Arial", 14), width=100)
        self.submit_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.next_button = ctk.CTkButton(self.frame_center_bottom, text="Next", command=self.logic.next_question, font=("Arial", 14), width=100)
        self.next_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.restart_button = ctk.CTkButton(self.frame_center_bottom, text="Restart Quiz/Settings", command=self.back_to_start_screen, font=("Arial", 14), width=100)

        self.hint_button = ctk.CTkButton(self.frame_center_bottom, text="Hint", command=self.logic.hint, font=("Arial", 14), width=100)
        self.hint_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.hint_button.configure(state="normal")

        self.skip_button = ctk.CTkButton(self.frame_center_bottom, text="Skip", command=self.logic.skip, font=("Arial", 14), width=100)
        self.skip_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        self.skip_button.configure(state="normal")

        self.logic.display_question()
        self.logic.start_timer() # start the timer


    def run(self):
        """Runs the GUI."""
        self.root.mainloop()

    def enable_submit_button(self, index):
        """Enables the submit button and disables the next button."""
        if self.next_button.cget('state') == 'disabled':
            self.submit_button.configure(state="normal") # aqui

    def get_current_player_name(self):
        """Returns the name of the current player."""
        return self.player1 if self.logic.current_player == 1 else self.player2

    def countdown(self, count):
        """Start the countdown timer."""
        pygame.mixer.stop()

        # Check if the timer should be active
        if not self.logic.timer_active:
            return  # Exit the method if the timer is not active

        # Stop any existing sounds and destroy the timer widget
        try:
            if self.tic_tac_sound and self.buzz_sound:
                self.tic_tac_sound.stop()
                self.buzz_sound.stop()
                self.timer.destroy()
        except:
            self.tic_tac_sound = pygame.mixer.Sound("tic-tac.wav")
            self.buzz_sound = pygame.mixer.Sound("buzz.mp3")

        # Create the timer label (only if necessary)
        self.timer = ctk.CTkLabel(self.frame_center_bottom, text="", font=("Helvetica", 28), text_color="black")
        self.timer.grid(row=1, column=1, padx=20, pady=20)  # Use Grid to position the widget
        self.tic_tac_sound.play(-1)

        def update_countdown(remaining):
            """Updates the countdown timer."""
            if remaining > 0:
                self.timer.configure(text=str(remaining))
                self.timer.after(1000, update_countdown, remaining - 1)
            else:
                self.tic_tac_sound.stop()
                if self.logic.timer_active:
                    self.buzz_sound.play()
                    self.timer.configure(text="Time's up!", text_color="red")
                    self.timer.after(3000, self.buzz_sound.stop)
                    self.next_button.configure(state="normal")
                    self.submit_button.configure(state="disabled")

        update_countdown(count)

    def exit(self):
        """ Exits the game. """
        sys.exit()

    def back_to_start_screen(self):
        """ Back to the start screen to select new players. """
        self.root.withdraw()
        StartScreen()

class ShowRulesDialog(ctk.CTkToplevel):
    """ Custom pop-up window to display the game rules. """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Rules")
        RootUtils.center_window(self, SIZE_WIDTH, SIZE_HEIGHT)
        self.grab_set()

        # Configure a grade principal
        self.grid_rowconfigure(0, weight=0)  # Espaço para o título
        self.grid_rowconfigure(1, weight=1)  # Espaço para o scroll_frame
        self.grid_rowconfigure(2, weight=0)  # Espaço para o botão "Close"
        self.grid_columnconfigure(0, weight=1)

        # Title: Welcome to Brain Up: The Learning Adventure!
        title_label = ctk.CTkLabel(
            self,
            text="Welcome to Brain Up: The Learning Adventure!",
            font=("Arial", 18, "bold"),
            text_color="blue"
        )
        title_label.grid(row=0, column=0, pady=7, sticky="ew")

        # Rules of the game
        rules_text = (
            "1. Select two players to start the game.\n\n"
            "2. Add new name if needed or delete it.\n\n"
            "3. Each player takes turns answering multiple-choice questions.\n\n"
            "4. Questions cover subjects like Science, English, and Māori Vocabulary. More subjects can be added.\n\n"
            "5. You have 15 seconds to answer each question as default, however it can be changed.\n\n"
            "6. Correct answers add 10 points. Incorrect answers subtract 5 points. Time's up? Your points stay as they are.\n\n"
            "7. Twice per game, you have the option to get a hint, however reduces add points by 50%. Wrong answers are not affected.\n\n"  
            "8. Twice per game, you have the option to skip a hard question and get a new one. The question will back later.\n\n"
            "9. The final question is bonus: get +20 points (or +10 points if a hint is used). Lose -10 if wrong. Time's up? Your points stay as they are. \n\n"
            "10. The player with the most scores wins.\n\n"
            "11. Check the ranking to see who has the most scores in all games (only Top 20).\n\n"
            "12. Setup options: time limit per question and number of questions per player can be changed.\n\n"
            "13. Have fun and challenge your brain while learning!"
        )

        # Display rules in a scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=SIZE_WIDTH - 40, height=SIZE_HEIGHT - 100)
        self.scroll_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        ctk.CTkLabel(
            self.scroll_frame,
            text=rules_text,
            font=("Arial", 14),
            justify="left",
            wraplength=SIZE_WIDTH - 55
        ).grid(row=0, column=0, pady=5, sticky="w")

        # Close button
        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            font=("Arial", 14),
            width=100
        )
        self.close_button.grid(row=2, column=0, pady=10)

class ShowRankingDialog(ctk.CTkToplevel):
    """ Custom pop-up window to display the ranking of players. """
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.title("Player Rankings")
        #self.geometry("450x600")
        RootUtils.center_window(self, SIZE_WIDTH, SIZE_HEIGHT)
        self.grab_set()

        # set the main grid configuration
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Title: TOP 20
        self.title_label = ctk.CTkLabel(self, text="TOP 20", font=("Arial", 20, "bold"), text_color="blue")
        self.title_label.grid(row=0, column=0, pady=10, sticky="ew")

        # Fetch rankings from the database
        rankings = self.db_manager.get_ranking()

        # Create a scrollable frame for rankings
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=450, height=250)
        self.scroll_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        if not rankings:
            # show message if no rankings are available
            ctk.CTkLabel(self.scroll_frame, text="No rankings available.", font=("Arial", 14)).grid(row=0, column=0,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        else:
            # Headers
            headers = ["Rank", "Player", "Age", "Date", "Score"]
            for col, header in enumerate(headers):
                header_label = ctk.CTkLabel(self.scroll_frame, text=header, font=("Arial", 12, "bold"), anchor="w")
                header_label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

            # Rows
            for idx, (player, age, date_score, score) in enumerate(rankings, start=1):
                # formating date
                date_object = datetime.datetime.strptime(date_score, "%Y-%m-%d %H:%M:%S")
                formatted_date = date_object.strftime("%d/%m/%Y %H:%M")

                # Column 1: Rank
                rank_label = ctk.CTkLabel(self.scroll_frame, text=f"{idx}.", font=("Arial", 12), anchor="w")
                rank_label.grid(row=idx, column=0, padx=5, pady=2, sticky="w")

                # Column 2: Player
                player_label = ctk.CTkLabel(self.scroll_frame, text=player, font=("Arial", 12), anchor="w")
                player_label.grid(row=idx, column=1, padx=5, pady=2, sticky="w")

                # Column 3: Age
                age_label = ctk.CTkLabel(self.scroll_frame, text=age, font=("Arial", 12), anchor="w")
                age_label.grid(row=idx, column=2, padx=5, pady=2, sticky="w")

                # Column 4: Date
                date_label = ctk.CTkLabel(self.scroll_frame, text=formatted_date, font=("Arial", 12), anchor="w")
                date_label.grid(row=idx, column=3, padx=5, pady=2, sticky="w")

                # Column 5: Score
                score_label = ctk.CTkLabel(self.scroll_frame, text=score, font=("Arial", 12), anchor="w")
                score_label.grid(row=idx, column=4, padx=5, pady=2, sticky="w")

            # Fit columns to the content
            for col in range(len(headers)):
                self.scroll_frame.grid_columnconfigure(col, weight=1)

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy, font=("Arial", 14), width=100)
        self.close_button.grid(row=2, column=0, pady=10)

class SetupDialog(ctk.CTkToplevel):
    """ Custom pop-up window for setup options. """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Setup")
        RootUtils.center_window(self, 385, 180)
        self.grab_set()
        self.db_manager = DataBase()
        limit_time = DataBase().update_global_settings()[0]
        number_question = DataBase().update_global_settings()[1]

        # Setup options
        ctk.CTkLabel(self, text="Game Settings:", font=("Arial", 16, "bold"), anchor="center" ).grid(row=0, column=0, sticky="nsew")

        # Time limit per question
        self.time_limit_label = ctk.CTkLabel(self, text="Time Limit per Question (seconds):", font=("Arial", 14))
        self.time_limit_label.grid(row=1, column=0, padx=5)

        self.time_limit_entry = ctk.CTkEntry(self, width=40)
        self.time_limit_entry.insert(0, limit_time)  # Default value
        self.time_limit_entry.grid(row=1, column=1, padx=5)

        # Number of questions
        self.n_questions_label = ctk.CTkLabel(self, text="Number of Questions per Player:", font=("Arial", 14))
        self.n_questions_label.grid(row=2, column=0)

        self.n_questions_entry = ctk.CTkEntry(self, width=40)
        self.n_questions_entry.insert(0, number_question)  # Default value
        self.n_questions_entry.grid(row=2, column=1)

        bottom_spacer = ctk.CTkFrame(self, height=10, fg_color="transparent")
        bottom_spacer.grid(row=3, pady=10)

        # Save button
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_settings, font=("Arial", 14), width=100)
        self.save_button.grid(row=4, column=0)

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy, font=("Arial", 14), width=100)
        self.close_button.grid(row=4, column=1)

    def save_settings(self):
        """ Save the settings and update the global LIMIT_TIME. """
        time_limit = self.time_limit_entry.get()
        num_question = self.n_questions_entry.get()
        self.db_manager.update_setup(time_limit, num_question)
        self.db_manager = DataBase()
        self.destroy()


class LastQuestionDialog(ctk.CTkToplevel):
    """ Custom pop-up window to inform that it's the last question. """

    def __init__(self, parent, player1, player2, current_player):
        super().__init__(parent)
        self.title("Bonus Question")
        RootUtils.center_window(self, 300, 200)  # size of window
        self.grab_set()  # turn on grab set

        # find the player of the round
        player_of_the_round = player1 if current_player == 1 else player2


        # Message
        message_label = ctk.CTkLabel(self, text="This is your last question!\n\n"
                                                "Bonus question!\n\n"
                                                "+20 points if correct\n"
                                                "(+10 using hint)\n"
                                                "-10 points if wrong", font=("Arial", 13))
        message_label.pack(pady=20)

        # OK Button
        ok_button = ctk.CTkButton(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10)

        # Wait for the window to close
        self.wait_window(self)

if __name__ == "__main__":
    StartScreen()
