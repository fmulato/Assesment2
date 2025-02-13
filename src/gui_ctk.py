import json
import customtkinter as ctk
import random  # Import necessário para selecionar questões aleatórias

SIZE_WIDTH = 800
SIZE_HEIGHT = 600


class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Game for Kids")
        master.geometry(f"{SIZE_WIDTH}x{SIZE_HEIGHT}")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Frames
        self.frame_left = ctk.CTkFrame(master, width=0.25 * SIZE_WIDTH)
        self.frame_center = ctk.CTkFrame(master, width=0.50 * SIZE_WIDTH)
        self.frame_right = ctk.CTkFrame(master, width=0.25 * SIZE_WIDTH)

        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_center.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.frame_right.pack(side="left", fill="y", padx=10, pady=10)

        # Fontes
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

        # Perguntas
        self.category_label = ctk.CTkLabel(self.frame_center, text="Category: ", font=font_categ, text_color='blue')
        self.category_label.pack(pady=5)
        self.question_label = ctk.CTkLabel(
            self.frame_center, text="Question will appear here", font=font_quest, wraplength=500
        )
        self.question_label.pack(pady=20)

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

        self.submit_button = ctk.CTkButton(
            self.frame_center, text="Submit", command=self.check_answer, font=("Arial", 14)
        )
        self.submit_button.pack(pady=20)

        # Carregar perguntas e selecionar duas aleatórias
        self.questions = self.load_questions("questions.json")
        self.selected_questions = random.sample(list(enumerate(self.questions, start=1)), 3)  # Seleciona 2 perguntas aleatórias
        self.current_question_index = 0

        self.display_question()

    def load_questions(self, file_path):
        """Carrega perguntas de um arquivo JSON."""
        with open(file_path, "r") as file:
            questions = json.load(file)
        return questions

    def display_question(self):
        """Exibe a pergunta atual e suas opções."""
        if self.current_question_index < len(self.selected_questions):
            question_number, question_data = self.selected_questions[self.current_question_index]

            # Atualiza a categoria
            self.category_label.configure(text=f"Category: {question_data['category']}")

            # Exibe a numeração da pergunta
            self.question_label.configure(text=f"{question_number}. {question_data['question']}")

            # Atualiza as opções
            for i, option in enumerate(question_data["options"]):
                self.option_buttons[i].configure(text=option)
                self.option_buttons[i]._value = str(i + 1)

            self.options_var.set(None)
        else:
            self.category_label.configure(text="Category: ")
            self.question_label.configure(text="No more questions!")
            for button in self.option_buttons:
                button.pack_forget()
            self.submit_button.pack_forget()

    def check_answer(self):
        """Verifica a resposta selecionada."""
        selected_option = self.options_var.get()
        _, question_data = self.selected_questions[self.current_question_index]
        correct_answer = question_data["correct_answer"]

        if selected_option == correct_answer:
            print("Correct!")
            self.score_player1 += 10
            self.score_player1_label.configure(text=f"Score: {self.score_player1}")
        else:
            print("Incorrect!")

        self.current_question_index += 1
        self.display_question()


if __name__ == "__main__":
    root = ctk.CTk()
    app = QuizApp(root)
    root.mainloop()
