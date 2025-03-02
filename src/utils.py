"""
This module contains utility functions to load questions into the database from a JSON file.
Verifies if a question already exists in the database. If it does, it skips the insertion.
"""""

import random
from typing import Sequence, List, Tuple
import customtkinter as ctk
from datetime import datetime

NUMBER_QUESTION = 2

class Utils:

    def select_random_elements(self, elements, n=NUMBER_QUESTION*2) -> List[Tuple[int, any]]:

        if not isinstance(elements, (list, tuple, set)):
            raise ValueError("The 'elements' argument must be a list, tuple, or set.")

        if n > len(elements):
            raise ValueError("The number of selected elements (m) cannot be greater than the total elements (n).")

        return random.sample(list(enumerate(elements, start=1)), n)

    # def shuffle_answers(self, options, correct_answer):
    #     """Shuffle the answers and return a new randomized list with the correct answer index updated."""
    #     indexed_options = list(enumerate(options))  # Attach original indices
    #     random.shuffle(indexed_options)  # Shuffle the options
    #
    #     # Extract shuffled options and find the new index of the correct answer
    #     shuffled_options = [option[1] for option in indexed_options]
    #     new_correct_index = [i for i, option in enumerate(indexed_options) if option[0] == correct_answer - 1][0] + 1
    #
    #     return shuffled_options, new_correct_index  # Return shuffled options & updated correct answer index
    #
    # def calculate_age(self, birthday):
    #     """ Calculate age from birth date. """
    #     birth_date = datetime.strptime(birthday, "%Y-%m-%d")
    #     today = datetime.today()
    #     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    #     return age

    def shuffle_answers(self, options, correct_answer):
        """Shuffle the answers and return a new randomized list with the correct answer index updated."""
        indexed_options = list(enumerate(options, start=1))  # Mantém os índices originais (1 a 4)
        random.shuffle(indexed_options)  # Embaralha as opções

        # create a dictionary to map the original index to the new index
        index_mapping = {orig_idx: new_idx + 1 for new_idx, (orig_idx, _) in enumerate(indexed_options)}

        # Find the new index of the correct answer
        new_correct_index = index_mapping[correct_answer]

        # Return shuffled options, updated correct answer index, and index
        shuffled_options = [option[1] for option in indexed_options]
        return shuffled_options, new_correct_index, index_mapping

class CustomPopup(ctk.CTkToplevel):
    """ Custom pop-up window for success and error messages """
    def __init__(self, title, message):
        super().__init__()
        self.title(title)

        from gui import RootUtils

        gui = RootUtils()
        window_width = 300
        window_height = 150
        gui.center_window(self, window_width, window_height)

        self.grab_set()  # Make modal

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=10)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)


