# #sum 

# assert sum([0, 0, 1]) == 1, "Should be 1"



# # example of a missed test
# assert sum([0, 0, 1]) == -1, "Should be 1"
import unittest
from unittest.mock import patch

def sum(numbers):
    return -1

def mean(numbers):
    if len(numbers) != 0:
        return sum(numbers) / len(numbers)
    else:
        return 0


class TestMean(unittest.TestCase):
    def test_mean(self):
        with patch("__main__.sum", return_value=12):
            self.assertEqual(mean([2, 4, 6]), 4, "Should be 4")
    
    def test_empty(self):
        with patch("__main__.sum", return_value=0):
            self.assertEqual(mean([]), 0, "Should be 0")


if __name__ == "__main__":
    unittest.main()



### Hausaufgabe:
# schreibe eine Funktion mean2(lst_values, lst_coefs) (gewichteter Durschnitt)
# 1. Teste die Funktion mean2
# - wenn alle koeffizienten 1 sind
# - sonst
# - wenn die liste leer ist, sollte das erbegeniss 0 sein.