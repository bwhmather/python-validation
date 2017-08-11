import unittest

import sys
from datetime import date, datetime

import six
import pytz

from validation import (
    validate_int, validate_bool,
    validate_text, validate_bytes,
    validate_date, validate_datetime
)


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


class ValidateTextTestCase(unittest.TestCase):
    def test_valid(self):
        validate_text(u"hello world")

    def test_bytestring(self):
        with self.assertRaises(TypeError):
            validate_text(b"hello world")

    def test_min_length(self):
        validate_text(u"123456", min_length=6)

        with self.assertRaises(ValueError):
            validate_text(u"123456", min_length=7)

    def test_max_length(self):
        validate_text(u"123456", max_length=6)

        with self.assertRaises(ValueError):
            validate_text(u"123456", max_length=5)

    def test_pattern(self):
        validate_text(u"a----b", pattern=r"a-*b")

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=r"end")

        with self.assertRaises(ValueError):
            validate_text(u"begin end", pattern=r"begin")

    def test_required(self):
        validate_text(None, required=False)

        with self.assertRaises(TypeError):
            validate_text(None)

    def test_closure(self):
        validator = validate_text(min_length=4)
        validator(u"12345")
        with self.assertRaises(ValueError):
            validator(u"123")


class ValidateBytesTestCase(unittest.TestCase):
    def test_valid(self):
        validate_bytes(b"deadbeaf")

    def test_unicode(self):
        with self.assertRaises(TypeError):
            validate_bytes(u"hello world")

    def test_min_length(self):
        validate_bytes(b"123456", min_length=6)

        with self.assertRaises(ValueError):
            validate_bytes(b"123456", min_length=7)

    def test_max_length(self):
        validate_bytes(b"123456", max_length=6)

        with self.assertRaises(ValueError):
            validate_bytes(b"123456", max_length=5)

    def test_required(self):
        validate_bytes(None, required=False)

        with self.assertRaises(TypeError):
            validate_bytes(None)

    def test_closure(self):
        validator = validate_bytes(min_length=4)
        validator(b"12345")
        with self.assertRaises(ValueError):
            validator(b"123")


class ValidateDateTestCase(unittest.TestCase):
    def test_valid(self):
        validate_date(date.today())

    def test_datetime(self):
        with self.assertRaises(TypeError):
            validate_date(datetime.now())

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_date("1970-01-01")

    def test_required(self):
        validate_date(None, required=False)

        with self.assertRaises(TypeError):
            validate_date(None)

    def test_closure(self):
        validator = validate_date()
        validator(date.today())
        with self.assertRaises(TypeError):
            validator(datetime.now())


class ValidateDateTimeTestCase(unittest.TestCase):
    def test_valid(self):
        validate_datetime(datetime.now(pytz.utc))

    def test_no_timezone(self):
        with self.assertRaises(ValueError):
            validate_datetime(datetime.now())

    def test_date(self):
        with self.assertRaises(TypeError):
            validate_datetime(date.today())

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_date("1970-01-01T12:00:00+00:00")

    def test_required(self):
        validate_date(None, required=False)

        with self.assertRaises(TypeError):
            validate_date(None)

    def test_closure(self):
        validator = validate_date()
        validator(date.today())
        with self.assertRaises(TypeError):
            validator(datetime.now())
