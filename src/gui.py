import customtkinter as ctk
#import quiz_logic as ql
from PIL import Image
import os
import pygame

#import user_management.py
from user_management import UserManagement

SIZE_WIDTH = 800
SIZE_HEIGHT = 600
LIMIT_TIME = 5

class RootUtils:
    @staticmethod
    def center_window(root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(width, height)
        root.maxsize(width, height)

class StartScreen:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Brain Up! - Registration")
        # Add user management instance
        self.user_manager = UserManagement()


        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Selected players list (Max 2 people)
        self.selected_players = []


        # Add New Name button
        self.add_name_button = ctk.CTkButton(self.root, text="Add New Name", command=self.add_new_name)
        self.add_name_button.grid(row=4, column=0, columnspan=4, pady=10)

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

        # Instructions

        # Configure columns to have equal weight for balanced spacing
        label_frame.columnconfigure(0, weight=1)  # Column for Player 1
        label_frame.columnconfigure(1, weight=1)  # Column for "VS"
        label_frame.columnconfigure(2, weight=1)  # Column for Player 2

        self.label_instructions = ctk.CTkLabel(label_frame, text="Please select players:", font=font_instruction,
                     text_color='blue')
        self.label_instructions.grid(row=0, column=1, pady=10)

        # Player 1:
        self.label_player1 = ctk.CTkLabel(label_frame, text="Player 1:", font=font_instruction, text_color='green')
        self.label_player1.grid(row=1, column=0, pady=5, sticky="ew")
        self.label_player1_age = ctk.CTkLabel(label_frame, text=self.age1, font=font_instruction, text_color='green')
        self.label_player1_age.grid(row=2, column=0, pady=5, sticky="ew")

        # versus
        self.label_vs = ctk.CTkLabel(label_frame, text="      VS      ", font=font_instruction, text_color='black')
        self.label_vs.grid(row=1, column=1, pady=5, sticky="ew")

        # Player 2:
        self.label_player2 = ctk.CTkLabel(label_frame, text="Player 2:", font=font_instruction, text_color='blue')
        self.label_player2.grid(row=1, column=2, pady=5, sticky="ew")
        self.label_player2_age = ctk.CTkLabel(label_frame, text=self.age2, font=font_instruction, text_color='blue')
        self.label_player2_age.grid(row=2, column=2, pady=5, sticky="ew")

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

        self.root.mainloop()

    def display_player_buttons(self):
        # Clear the button frame, before adding new buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        players = self.user_manager.get_all_players()

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

        # Update player names and ages
        if len(self.selected_players) == 2:
            self.player1, self.age1 = self.selected_players[0]
            self.player2, self.age2 = self.selected_players[1]

    def add_new_name(self):
        #AddNameDialog(self.root, self.user_manager)
        #AddNameDialog(self, self.user_manager)
        AddNameDialog(self.root, self.user_manager, self)

    def update_buttons(self):
        pass


    def start_game(self):
        """ Start the game with selected players. """
        if len(self.selected_players) != 2:
            return  # Ensure exactly two players are selected

        player1, age1 = self.selected_players[0]
        player2, age2 = self.selected_players[1]

        print(f"Starting game with: {player1} ({age1}) vs {player2} ({age2})")

        # Hide current screen
        self.root.withdraw()

        # Open the game window (Assuming you have a game class)
        game_window = ctk.CTk()
        game = Gui(game_window, player1, age1, player2, age2)  # Assuming `Gui` is your game class
        game.run()

class AddNameDialog(ctk.CTkToplevel):
    """ Custom pop-up window for entering Name and Date of Birth using only customtkinter. """
    def __init__(self, parent, user_manager, start_screen):
        super().__init__(parent)  # Use parent (self.root) para CTkToplevel
        self.user_manager = user_manager
        self.start_screen = start_screen  # Referência à instância de StartScreen
        self.parent = parent  # Inicializa o atributo 'parent' corretamente
        self.result = None

        self.title("Add New Player")

        window_width = 300
        window_height = 200
        RootUtils.center_window(self, window_width, window_height)

        self.grab_set()  # Make the window modal (force user interaction)

        ctk.CTkLabel(self, text="Name:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Birthday (YYYY-MM-DD):").pack(pady=5)
        self.birthday_entry = ctk.CTkEntry(self)
        self.birthday_entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(self, text="OK", command=self.apply)
        self.submit_button.pack(pady=10)

    def apply(self):
        """ Save input values when OK is pressed """
        name = self.name_entry.get()
        birthday = self.birthday_entry.get()

        if not name or not birthday:
            CustomPopup(self, "Error", "Both fields are required.")
            return

        success = self.user_manager.register_user(name, birthday)
        if success:
            age = self.user_manager.calculate_age(birthday)
            self.user_manager.save_age_to_scores(name, age)
            CustomPopup(self, "Success",
                        f"User {name} added successfully with age {age}!")
            self.start_screen.display_player_buttons()  # Use a referência ao StartScreen
            self.destroy()  # Close the pop-up after success

class CustomPopup(ctk.CTkToplevel):
    """ Custom pop-up window for success and error messages """
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)

        window_width = 300
        window_height = 200
        RootUtils.center_window(self, window_width, window_height)

        #self.geometry("300x150")
        self.grab_set()  # Make modal

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=10)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)



class Gui:
    def __init__(self, root, player1='Player 1', age1="", player2='Player 2', age2=""):
        # Create the main window
        self.root = root
        self.root.title("Brain Up! Quiz Game")

        self.player1 = player1
        self.age1 = age1
        self.player2 = player2
        self.age2 = age2

        pygame.mixer.init()

        # Code for the Gui class
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Force the main window to appear centered on the screen
        RootUtils.center_window(self.root, SIZE_WIDTH, SIZE_HEIGHT)

        #self.logic = ql.Logic(self)

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

        # Player 1
        self.player1_label = ctk.CTkLabel(self.frame_left, text=f" Player 1: {self.player1} ({self.age1})",
                                          font=font_player)
        self.player1_label.pack(pady=10)
        self.score_player1 = 0
        self.score_player1_label = ctk.CTkLabel(self.frame_left, text=f" Score: {self.score_player1} ",
                                                font=font_score)
        self.score_player1_label.pack(pady=5)

        # Player 2
        self.player2_label = ctk.CTkLabel(self.frame_right, text=f" Player 2: {self.player2} ({self.age2})",
                                          font=font_player)
        self.player2_label.pack(pady=10)
        self.score_player2 = 0
        self.score_player2_label = ctk.CTkLabel(self.frame_right, text=f" Score: {self.score_player2} ",
                                                font=font_score)
        self.score_player2_label.pack(pady=5)

        # Questions
        self.category_label = ctk.CTkLabel(self.frame_center_top, text="Category:", font=font_categ, text_color='blue')
        self.category_label.pack(pady=5)
        self.question_label = ctk.CTkLabel(
            self.frame_center_top, text="Question will appear here", font=font_quest, wraplength=500)
        self.question_label.pack(pady=20)

        # Results
        self.winner_label = ctk.CTkLabel(self.frame_center_middle, text="Winner:", font=font_categ, text_color='green')
        self.result_label = ctk.CTkLabel(self.frame_center_middle, text="", font=("Arial", 16), text_color="black")
        self.result_label.pack(pady=10)

        # Load questions
        # self.logic.save_player_info()
        # self.questions = self.logic.load_questions("questions.json")
        # self.selected_questions = select_random_elements(self.questions)
        self.current_question_index = 0
        # self.logic.display_question()... # Frame for buttons
        self.frame_center_bottom.grid_columnconfigure(0, weight=1)
        self.frame_center_bottom.grid_columnconfigure(1, weight=1)
        self.frame_center_bottom.grid_columnconfigure(2, weight=1)

        self.submit_button = ctk.CTkButton(self.frame_center_bottom, text="Submit",
                                           font=("Arial", 14), width=100)
        #command=self.logic.check_answer,
        self.submit_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.next_button = ctk.CTkButton(self.frame_center_bottom, text="Next",
                                         command=lambda: self.countdown(LIMIT_TIME), font=("Arial", 14), width=100)
        #command = self.logic.next_question,
        self.next_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # self.next_button.grid_forget()

        self.restart_button = ctk.CTkButton(self.frame_center_bottom, text="Restart Quiz",
                                            font=("Arial", 14), width=100)
        #command=self.logic.restart_quiz,
        self.restart_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        # self.restart_button.grid_forget()

        self.exit_button = ctk.CTkButton(self.frame_center_bottom, text="Exit",
                                            command=self.exit, font=("Arial", 14), width=100)
        self.exit_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        # self.restart_button.grid_forget()

        self.config_button = ctk.CTkButton(self.frame_center_bottom, text="Setup",
                                         command=self.config, font=("Arial", 14), width=100)
        self.config_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # self.restart_button.grid_forget()

        self.timer = ctk.CTkLabel(self.frame_center_bottom, font=("Arial", 24))
        self.timer.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.timer.grid_forget()

    def run(self):
        self.root.mainloop()

    def countdown(self, count):
        self.timer.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.timer.configure(text=str(count), text_color="red")

        if count > 0:
            self.root.after(1000, self.countdown, count - 1)

            if count == LIMIT_TIME:
                pygame.mixer.music.load("tic-tac.mp3")
                pygame.mixer.music.play(loops=-1, fade_ms=500)

        else:
            self.timer.configure(text="Time's up!")
            pygame.mixer.music.stop()
            pygame.mixer.music.load("buzz.mp3")
            pygame.mixer.music.play()

    def exit(self):
        quit()


    def config(self):
        pass
