import unittest

from validation import validate_bool


class ValidateBoolTestCase(unittest.TestCase):
    def test_valid(self):
        validate_bool(True)
        validate_bool(False)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            validate_bool(1)

        with self.assertRaises(TypeError):
            validate_bool(0)

        with self.assertRaises(TypeError):
            validate_bool("true")

    def test_required(self):
        validate_bool(None, required=False)

        with self.assertRaises(TypeError):
            validate_bool(None)

    def test_closure(self):
        validator = validate_bool()
        validator(False)
        with self.assertRaises(TypeError):
            validator("false")

    def test_repr(self):
        validator = validate_bool(required=False)
        self.assertEqual(
            repr(validator),
            'validate_bool(required=False)',
        )
