import unittest

import math
import sys

import six

from validation import validate_int, validate_float


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

    def test_repr(self):
        validator = validate_int(min_value=1, max_value=1, required=False)
        self.assertEqual(
            repr(validator),
            'validate_int(min_value=1, max_value=1, required=False)',
        )


class ValidateFloatTestCase(unittest.TestCase):
    def test_valid(self):
        validate_float(1.0)
        validate_float(math.pi)

    def test_int(self):
        with self.assertRaises(TypeError):
            validate_float(1)

    def test_allow_inf(self):
        validate_float(float('inf'), allow_infinite=True)
        validate_float(float('-inf'), allow_infinite=True)

    def test_allow_nan(self):
        validate_float(float('nan'), allow_nan=True)
        validate_float(
            float('nan'), min_value=0.0, max_value=1.0, allow_nan=True,
        )

    def test_disallow_float(self):
        with self.assertRaises(ValueError):
            validate_float(float('inf'))

        with self.assertRaises(ValueError):
            validate_float(float('-inf'))

    def test_disallow_nan(self):
        with self.assertRaises(ValueError):
            validate_float(float('nan'))

    def test_min(self):
        validate_float(5.0, min_value=4.5)

        with self.assertRaises(ValueError):
            validate_float(5.0, min_value=5.5)

    def test_max(self):
        validate_float(5.0, max_value=5.5)

        with self.assertRaises(ValueError):
            validate_float(5.0, max_value=4.5)

    def test_required(self):
        validate_float(None, required=False)

        with self.assertRaises(TypeError):
            validate_float(None)

    def test_closure(self):
        validator = validate_float(min_value=0.0)
        with self.assertRaises(ValueError):
            validator(-1.0)

    def test_repr(self):
        validator = validate_float(
            min_value=1.0, max_value=1.0, required=False,
        )
        self.assertEqual(
            repr(validator),
            'validate_float(min_value=1.0, max_value=1.0, required=False)',
        )

        validator = validate_float(allow_infinite=True, allow_nan=True)
        self.assertEqual(
            repr(validator),
            'validate_float(allow_infinite=True, allow_nan=True)',
        )
