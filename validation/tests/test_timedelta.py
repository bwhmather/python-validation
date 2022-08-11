import unittest
from datetime import timedelta

from validation import validate_timedelta


class ValidateDateTimeTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_timedelta(timedelta(days=7))

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_timedelta("10 days")

    def test_not_required(self):  # type: () -> None
        validate_timedelta(None, required=False)

    def test_required(self):
        with self.assertRaises(TypeError):
            validate_timedelta(None)

    def test_closure_valid(self):  # type: () -> None
        validator = validate_timedelta()
        validator(timedelta(minutes=4))

    def test_min_value_valid(self):
        validate_timedelta(
            timedelta(minutes=0), min_value=timedelta(minutes=0)
        )

    def test_min_value_invalid(self):
        validate_timedelta(timedelta(days=-1), min_value=timedelta())

    def test_max_value_valid(self):
        validate_timedelta(
            timedelta(minutes=0), max_value=timedelta(minutes=0)
        )

    def test_max_value_invalid(self):
        validate_timedelta(timedelta(days=1), max_value=timedelta())

    def test_repr(self):  # type: () -> None
        validator = validate_timedelta()
        self.assertEqual(
            repr(validator),
            'validate_timedelta()',
        )

        validator = validate_timedelta(required=False)
        self.assertEqual(
            repr(validator),
            'validate_timedelta(required=False)',
        )
