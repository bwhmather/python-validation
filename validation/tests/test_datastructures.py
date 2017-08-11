import unittest

from validation import (
    validate_int, validate_text,
    validate_list, validate_set,
    validate_dict,
)


class ValidateListTestCase(unittest.TestCase):
    def test_empty_is_not_missing(self):
        validate_list([])

    def test_non_empty_no_validator(self):
        validate_list([1, 'string'])

    def test_validator_valid(self):
        validate_list([1, 2, 3], validator=validate_int())

    def test_validator_invalid(self):
        with self.assertRaises(ValueError):
            validate_list([1, 2, 3, -1], validator=validate_int(min_value=0))

    def test_validate_set(self):
        with self.assertRaises(TypeError):
            validate_list({1}, validator=validate_int())

    def test_validate_iterator(self):
        with self.assertRaises(TypeError):
            validate_list(iter([1]), validator=validate_int())

    def test_min_len(self):
        validate_list([1, 2, 3], min_length=3)

        with self.assertRaises(ValueError):
            validate_list([1, 2, 3], min_length=4)

    def test_max_len(self):
        validate_list([1, 2, 3], max_length=3)

        with self.assertRaises(ValueError):
            validate_list([1, 2, 3, 4], max_length=3)

    def test_required(self):
        validate_list(None, required=False)

        with self.assertRaises(TypeError):
            validate_list(None)

    def test_closure(self):
        validator = validate_list(max_length=3)
        validator([1])
        with self.assertRaises(ValueError):
            validator([1, 2, 3, 4])


class ValidateSetTestCase(unittest.TestCase):
    def test_empty_is_not_missing(self):
        validate_set(set())

    def test_non_empty_no_validator(self):
        validate_set({1, 'string'})

    def test_validator_valid(self):
        validate_set({1, 2, 3}, validator=validate_int())

    def test_validator_invalid(self):
        with self.assertRaises(ValueError):
            validate_set({1, 2, 3, -1}, validator=validate_int(min_value=0))

    def test_validate_list(self):
        with self.assertRaises(TypeError):
            validate_set([1], validator=validate_int())

    def test_min_len(self):
        validate_set({1, 2, 3}, min_length=3)

        with self.assertRaises(ValueError):
            validate_set({1, 2, 3}, min_length=4)

    def test_max_len(self):
        validate_set({1, 2, 3}, max_length=3)

        with self.assertRaises(ValueError):
            validate_set({1, 2, 3, 4}, max_length=3)

    def test_required(self):
        validate_set(None, required=False)

        with self.assertRaises(TypeError):
            validate_set(None)

    def test_closure(self):
        validator = validate_set(max_length=3)
        validator({1})
        with self.assertRaises(ValueError):
            validator({1, 2, 3, 4})


class ValidateTupleTestCase(unittest.TestCase):
    pass


class ValidateDictTestCase(unittest.TestCase):
    def test_basic_valid(self):
        validate_dict({'hello': "world"})

    def test_schema_valid(self):
        validator = validate_dict(schema={
            'hello': validate_text(),
            'count': validate_int(),
        })

        validator({'hello': u"world", 'count': 2})

    def test_schema_invalid_value_type(self):
        validator = validate_dict(schema={
            'hello': validate_text(),
            'count': validate_int(),
        })

        with self.assertRaises(TypeError):
            validator({
                'hello': u"world",
                'count': "one hundred",
            })

    def test_schema_invalid_value(self):
        validator = validate_dict(schema={
            'hello': validate_text(),
            'count': validate_int(min_value=0),
        })

        with self.assertRaises(ValueError):
            validator({
                'hello': u"world",
                'count': -1,
            })

    def test_schema_unexpected_key(self):
        validator = validate_dict(schema={
            'expected': validate_int(),
        })

        with self.assertRaises(ValueError):
            validator({
                'expected': 1,
                'unexpected': 2,
            })

    def test_schema_allow_extra(self):
        validator = validate_dict(schema={
            'expected': validate_int(),
        }, allow_extra=True)

        validator({
            'expected': 1,
            'unexpected': 2,
        })


class ValidateEnumTestCase(unittest.TestCase):
    pass
