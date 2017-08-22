import unittest

from . import (
    test_core,
    test_number,
    test_string,
    test_datetime,
    test_datastructure,
)


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_core),  # type: ignore
    loader.loadTestsFromModule(test_number),  # type: ignore
    loader.loadTestsFromModule(test_string),  # type: ignore
    loader.loadTestsFromModule(test_datetime),  # type: ignore
    loader.loadTestsFromModule(test_datastructure),  # type: ignore
))
