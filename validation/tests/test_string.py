import unittest
import re

from validation import validate_text, validate_bytes


class ValidateTextTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_text(u"hello world")

    def test_bytestring(self):
        with self.assertRaises(TypeError):
            validate_text(b"hello world")

    def test_min_length(self):  # type: () -> None
        validate_text(u"123456", min_length=6)

        with self.assertRaises(ValueError):
            validate_text(u"123456", min_length=7)

    def test_max_length(self):  # type: () -> None
        validate_text(u"123456", max_length=6)

        with self.assertRaises(ValueError):
            validate_text(u"123456", max_length=5)

    def test_pattern(self):  # type: () -> None
        validate_text(u"a----b", pattern=r"a-*b")

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=r"end")

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=r"begin")

    def test_precompiled_pattern(self):  # type: () -> None
        validate_text(u"a----b", pattern=re.compile(r"a-*b"))

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=re.compile(r"end"))

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=re.compile(r"begin"))

    def test_required(self):  # type: () -> None
        validate_text(None, required=False)

        with self.assertRaises(TypeError):
            validate_text(None)

    def test_closure(self):  # type: () -> None
        validator = validate_text(min_length=4)
        validator(u"12345")
        with self.assertRaises(ValueError):
            validator(u"123")

    def test_repr(self):  # type: () -> None
        validator = validate_text(pattern='hello world', required=False)
        self.assertEqual(
            repr(validator),
            'validate_text(pattern=\'hello world\', required=False)',
        )

        validator = validate_text(min_length=4, max_length=10)
        self.assertEqual(
            repr(validator),
            'validate_text(min_length=4, max_length=10)',
        )

    def test_check_requested_bounds(self):
        with self.assertRaises(TypeError):
            validate_text(min_length='1')

        with self.assertRaises(ValueError):
            validate_text(min_length=-1)

        with self.assertRaises(TypeError):
            validate_text(max_length='1')

        with self.assertRaises(ValueError):
            validate_text(max_length=-1)

        with self.assertRaises(ValueError):
            validate_text(min_length=10, max_length=9)


class ValidateBytesTestCase(unittest.TestCase):
    def test_valid(self):  # type: () -> None
        validate_bytes(b"deadbeaf")

    def test_unicode(self):
        with self.assertRaises(TypeError):
            validate_bytes(u"hello world")

    def test_min_length(self):  # type: () -> None
        validate_bytes(b"123456", min_length=6)

        with self.assertRaises(ValueError):
            validate_bytes(b"123456", min_length=7)

    def test_max_length(self):  # type: () -> None
        validate_bytes(b"123456", max_length=6)

        with self.assertRaises(ValueError):
            validate_bytes(b"123456", max_length=5)

    def test_required(self):  # type: () -> None
        validate_bytes(None, required=False)

        with self.assertRaises(TypeError):
            validate_bytes(None)

    def test_closure(self):  # type: () -> None
        validator = validate_bytes(min_length=4)
        validator(b"12345")
        with self.assertRaises(ValueError):
            validator(b"123")

    def test_repr(self):  # type: () -> None
        validator = validate_bytes(min_length=4, max_length=10, required=False)
        self.assertEqual(
            repr(validator),
            'validate_bytes(min_length=4, max_length=10, required=False)',
        )

    def test_check_requested_bounds(self):
        with self.assertRaises(TypeError):
            validate_bytes(min_length='1')

        with self.assertRaises(ValueError):
            validate_bytes(min_length=-1)

        with self.assertRaises(TypeError):
            validate_bytes(max_length='1')

        with self.assertRaises(ValueError):
            validate_bytes(max_length=-1)

        with self.assertRaises(ValueError):
            validate_bytes(min_length=10, max_length=9)
