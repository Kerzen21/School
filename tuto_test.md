# Software testing

Tests can either be automated or manual:
- Manuel testing: produce a list of features to test and for each feature the types of input value and the expected results
- Automatated testing: just as manual testing, automated testing required for each feature to be tested (functions,...) input values and expected results.

## Types of tests
Tests can be *passive*, when the code is just read and analysed by a human, or *dynamic*, when the code is executed.

Another distinction is *black box* and *white box* testing:
- black box tests: The tests are done only with the knowledge of what the software is expected produce for a given result.
- white box tests: Tests are designed by taking the internal implementation of the software in consideration.


### Unit Tests
[Unit testing](https://en.wikipedia.org/wiki/Unit_testing) checks the functionality of individual units, whit the consideration that their dependancies are working.
### Integration Tests
[Integration tests](https://en.wikipedia.org/wiki/Integration_testing) check how well assembled unitss work togheter to produce the expected results.
*Note* Unlike unit tests,   the goal of integration tests isn't to show which specific unit is not working as expected.


## Testing with python

### Assertions
Testing can be done with python as follows:
```Python
assert sum([2, 4, 6]) == 12, "Should be 12"
```
If the assertion that the result of the function call is 12 is True, the test is successful and nothing happens. Otherwise, the program stop the message `Should be 12`.

A convention is to put tests in files with names starting with `test_...`
```Python
#File test_sum.py

def test_sum():
    assert sum([2, 4, 6]) == 12, "Should be 12"

if __name__ == "__main__":
    test_sum()
    print("Done with tests")
```
### Module unittest
Python provides the `unittest` module for elaborated tests.
When using the unittest module, tests are build.
```Python
import unittest

class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum([2, 4, 6]), 12, "Should be 12")
    
    def test_sum_empty(self):
        self.assertEqual(sum([]), 0, "Should be 0")


if __name__ == "__main__":
    unittest.main()
```

A [Mock](https://en.wikipedia.org/wiki/Mock_object) is an object that mimic the behavior of real objects in controlled ways.

For unit testing, mock objects are used to avoid runing already tested units or dependancies in unit test. The function "patch"
```Python
import unittest
from unittest.mock import patch


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
```




For more details:
- [Software Testing, Wikipedia](https://en.wikipedia.org/wiki/Software_testing)
- [Python testing, Real Python](https://realpython.com/python-testing/)
- [Unittest - Unit testing framework, Python](https://docs.python.org/3/library/unittest.html)
- [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)