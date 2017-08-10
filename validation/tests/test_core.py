import unittest

import sys

import six

from validation import validate_int


class ValidateIntTestCase(unittest.TestCase):
    def test_valid(self):
        validate_int(0)
        validate_int(1)

    def test_long(self):
        if six.PY3:
            raise unittest.SkipTest("not relevant in python3")

        validate_int(2 * sys.maxint)  # pylint: disable=no-member
        validate_int(-2 * sys.maxint)  # pylint: disable=no-member

    def test_float(self):
        with self.assertRaises(TypeError):
            validate_int(1.0)

    def test_min(self):
        validate_int(5, min_value=5)

        with self.assertRaises(ValueError):
            validate_int(5, min_value=6)

    def test_max(self):
        validate_int(5, max_value=5)

        with self.assertRaises(ValueError):
            validate_int(5, max_value=4)

    def test_required(self):
        validate_int(None, required=False)

        with self.assertRaises(TypeError):
            validate_int(None)

    def test_closure(self):
        validator = validate_int(min_value=0)
        with self.assertRaises(ValueError):
            validator(-1)


class ValidateFloatTestCase(unittest.TestCase):
    pass


class ValidateBoolTestCase(unittest.TestCase):
    pass


class ValidateTextTestCase(unittest.TestCase):
    pass


class ValidateBytesTestCase(unittest.TestCase):
    pass


class ValidateDateTestCase(unittest.TestCase):
    pass


class ValidateDateTimeTestCase(unittest.TestCase):
    pass
