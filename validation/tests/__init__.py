import unittest

from . import test_core, test_datastructures


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_core),  # type: ignore
    loader.loadTestsFromModule(test_datastructures),  # type: ignore
))
