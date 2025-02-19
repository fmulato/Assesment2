import random
from typing import Sequence, List, Tuple

NUMBER_QUESTION = 5

def select_random_elements(elements: Sequence,  n: int = NUMBER_QUESTION) -> List[Tuple[int, any]]:

    if not isinstance(elements, (list, tuple, set)):
        raise ValueError("The 'elements' argument must be a list, tuple, or set.")

    elements = list(elements)  # Ensures it is a list to support indexing

    if n > len(elements):
        raise ValueError("The number of selected elements (m) cannot be greater than the total elements (n).")

    return random.sample(list(enumerate(elements, start=1)), n)