from __future__ import absolute_import

from . import unittest
import tempfile

from validation import validate_text_file


class ValidateTextFileTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        
        validate_date(open()

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
