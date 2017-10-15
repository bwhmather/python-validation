import unittest

import math
import sys

import six

from validation import validate_int, validate_float


class ValidateIntTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
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

    def test_min(self):  # type: () -> None
        validate_int(5, min_value=5)

        with self.assertRaises(ValueError):
            validate_int(5, min_value=6)

    def test_max(self):  # type: () -> None
        validate_int(5, max_value=5)

        with self.assertRaises(ValueError):
            validate_int(5, max_value=4)

    def test_required(self):  # type: () -> None
        validate_int(None, required=False)

        with self.assertRaises(TypeError):
            validate_int(None)

    def test_closure(self):  # type: () -> None
        validator = validate_int(min_value=0)
        with self.assertRaises(ValueError):
            validator(-1)

    def test_repr(self):  # type: () -> None
        validator = validate_int(min_value=1, max_value=1, required=False)
        self.assertEqual(
            repr(validator),
            'validate_int(min_value=1, max_value=1, required=False)',
        )


class ValidateFloatTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_float(1.0)
        validate_float(math.pi)

    def test_int(self):
        with self.assertRaises(TypeError):
            validate_float(1)

    def test_allow_inf(self):  # type: () -> None
        validate_float(float('inf'), allow_infinite=True)
        validate_float(float('-inf'), allow_infinite=True)

    def test_allow_positive_inf_with_bounds(self):
        validate_float(float('inf'), min_value=0.0, allow_infinite=True)

        with self.assertRaises(ValueError):
            validate_float(float('inf'), max_value=0.0, allow_infinite=True)

        # Passing infinite as the upper bound suggests that the user doesn't
        # want an upper bound.  Infinite should be acceptable.
        validate_float(
            float('inf'), max_value=float('inf'), allow_infinite=True,
        )
        # Allowing only positive infinite when the minimum value is positive
        # infinite is the only behaviour that could reasonably be considered
        # useful.
        validate_float(
            float('inf'), min_value=float('inf'), allow_infinite=True,
        )

    def test_allow_negative_inf_with_bounds(self):
        validate_float(float('-inf'), max_value=0.0, allow_infinite=True)

        with self.assertRaises(ValueError):
            validate_float(float('-inf'), min_value=0.0, allow_infinite=True)

        # Passing infinite as the lower bound suggests that the user doesn't
        # want a lower bound.  Negative infinite should be acceptable.
        validate_float(
            float('-inf'), min_value=float('-inf'), allow_infinite=True,
        )
        # Allowing only negative infinite when the maximum value is negative
        # infinite is the only behaviour that could reasonably be considered
        # useful.
        validate_float(
            float('-inf'), max_value=float('-inf'), allow_infinite=True,
        )

    def test_allow_nan(self):  # type: () -> None
        validate_float(float('nan'), allow_nan=True)

    def test_allow_nan_with_bounds(self):
        validate_float(
            float('nan'), min_value=-1.0, max_value=1.0, allow_nan=True,
        )
        validate_float(
            float('nan'),
            min_value=float('-inf'), max_value=float('inf'),
            allow_nan=True,
        )

    def test_disallow_infinite(self):  # type: () -> None
        with self.assertRaises(ValueError):
            validate_float(float('inf'))

        with self.assertRaises(ValueError):
            validate_float(float('-inf'))

    def test_disallow_nan(self):  # type: () -> None
        with self.assertRaises(ValueError):
            validate_float(float('nan'))

    def test_min(self):  # type: () -> None
        validate_float(5.0, min_value=4.5)

        with self.assertRaises(ValueError):
            validate_float(5.0, min_value=5.5)

    def test_max(self):  # type: () -> None
        validate_float(5.0, max_value=5.5)

        with self.assertRaises(ValueError):
            validate_float(5.0, max_value=4.5)

    def test_required(self):  # type: () -> None
        validate_float(None, required=False)

        with self.assertRaises(TypeError):
            validate_float(None)

    def test_closure(self):  # type: () -> None
        validator = validate_float(min_value=0.0)
        with self.assertRaises(ValueError):
            validator(-1.0)

    def test_repr(self):  # type: () -> None
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
