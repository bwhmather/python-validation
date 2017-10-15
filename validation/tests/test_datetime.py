import unittest

from datetime import date, datetime

import pytz

from validation import (
    validate_date, validate_datetime
)


class ValidateDateTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_date(date.today())

    def test_datetime(self):
        with self.assertRaises(TypeError):
            validate_date(datetime.now())

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_date("1970-01-01")

    def test_required(self):  # type: () -> None
        validate_date(None, required=False)

        with self.assertRaises(TypeError):
            validate_date(None)

    def test_closure(self):
        validator = validate_date()
        validator(date.today())
        with self.assertRaises(TypeError):
            validator(datetime.now())

    def test_repr(self):  # type: () -> None
        validator = validate_date(required=False)
        self.assertEqual(
            repr(validator),
            'validate_date(required=False)',
        )


class ValidateDateTimeTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_datetime(datetime.now(pytz.utc))

    def test_no_timezone(self):  # type: () -> None
        with self.assertRaises(ValueError):
            validate_datetime(datetime.now())

    def test_date(self):
        with self.assertRaises(TypeError):
            validate_datetime(date.today())

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_date("1970-01-01T12:00:00+00:00")

    def test_required(self):  # type: () -> None
        validate_date(None, required=False)

        with self.assertRaises(TypeError):
            validate_date(None)

    def test_closure(self):
        validator = validate_date()
        validator(date.today())
        with self.assertRaises(TypeError):
            validator(datetime.now())

    def test_repr(self):  # type: () -> None
        validator = validate_datetime()
        self.assertEqual(
            repr(validator),
            'validate_datetime()',
        )
