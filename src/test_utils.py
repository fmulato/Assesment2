
import pytest
from utils import Utils

def test_calculate_age():
    utils_instance = Utils()
    assert utils_instance.calculate_age("1976-09-09") == 48
    assert utils_instance.calculate_age("2012-06-09") == 12
    assert utils_instance.calculate_age("2024-01-01") == 1



