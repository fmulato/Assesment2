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

    def select_random_elements(self, elements, n=NUMBER_QUESTION) -> List[Tuple[int, any]]:

        if not isinstance(elements, (list, tuple, set)):
            raise ValueError("The 'elements' argument must be a list, tuple, or set.")

        if n > len(elements):
            raise ValueError("The number of selected elements (m) cannot be greater than the total elements (n).")

        return random.sample(list(enumerate(elements, start=1)), n)


    def shuffle_answers(self, options):
        """Shuffle the answers to display them in a random order."""
        # todo: implement this method
        pass

    def calculate_age(self, birthday):
        """ Calculate age from birth date. """
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

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


