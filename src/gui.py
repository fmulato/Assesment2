import json
import tkinter as tk

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Game for Kids")
        master.geometry("800x600")  # Set the window size to 800x600

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)  # Add some vertical padding

        # Question label
        self.question_label = tk.Label(self.frame, text="Question will appear here", font=("Arial", 16))
        self.question_label.pack(pady=20)  # Add some vertical padding

        # Variable to hold the selected option
        self.options_var = tk.StringVar()

        # Radio buttons for answer options
        self.option_buttons = []
        for i in range(4):
            option_button = tk.Radiobutton(self.frame, text=f"Option {i + 1}", variable=self.options_var,
                                           value=str(i + 1), font=("Arial", 14))
            option_button.pack(anchor='w', padx=20)  # Align to the left with padding
            self.option_buttons.append(option_button)

        # Submit button
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.check_answer, font=("Arial", 14))
        self.submit_button.pack(pady=20)

        # Load questions from JSON
        self.questions = self.load_questions("questions.json")
        self.current_question_index = 0
        self.display_question()

    def load_questions(self, file_path):
        """Load questions from a JSON file."""
        with open(file_path, 'r') as file:
            questions = json.load(file)
        return questions

    def display_question(self):
        """Display the current question and its options."""
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data['question'])
            for i, option in enumerate(question_data['options']):
                self.option_buttons[i].config(text=option, value=str(i + 1))
            self.options_var.set(None)  # Reset the selected option
        else:
            self.question_label.config(text="No more questions!")
            for button in self.option_buttons:
                button.pack_forget()  # Hide option buttons if no more questions

    def check_answer(self):
        selected_option = self.options_var.get()
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        if selected_option == correct_answer:
            print("Correct!")
        else:
            print("Incorrect!")

        # Move to the next question
        self.current_question_index += 1
        self.display_question()
