import unittest

from . import (
    test_bool,
    test_int,
    test_float,
    test_text,
    test_bytes,
    test_date,
    test_datetime,
    test_datastructure,
)


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_bool),  # type: ignore
    loader.loadTestsFromModule(test_int),  # type: ignore
    loader.loadTestsFromModule(test_float),  # type: ignore
    loader.loadTestsFromModule(test_text),  # type: ignore
    loader.loadTestsFromModule(test_bytes),  # type: ignore
    loader.loadTestsFromModule(test_date),  # type: ignore
    loader.loadTestsFromModule(test_datetime),  # type: ignore
    loader.loadTestsFromModule(test_datastructure),  # type: ignore
))
