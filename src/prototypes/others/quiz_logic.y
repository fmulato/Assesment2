import json

class QuizManager:
    def __init__(self, file_path):
        self.questions = self.load_questions(file_path)
        self.current_question_index = 0
        self.score_player1 = 0
        self.score_player2 = 0

    def load_questions(self, file_path):
        """Load questions from a JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    def get_current_question(self):
        """Return the current question data."""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, selected_option):
        """Check if the selected option is correct and update the score."""
        current_question = self.get_current_question()
        if current_question and selected_option == current_question['correct_answer']:
            self.score_player1 += 10
            return True
        return False

    def next_question(self):
        """Move to the next question."""
        self.current_question_index += 1