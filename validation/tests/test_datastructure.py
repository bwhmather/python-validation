import unittest

from validation import (
    validate_int, validate_text,
    validate_list, validate_set,
    validate_mapping, validate_structure,
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

    def test_repr(self):
        validator = validate_list(min_length=1, max_length=100)
        self.assertEqual(
            repr(validator),
            'validate_list(min_length=1, max_length=100)',
        )

        validator = validate_list(validator=validate_int(), required=False)
        self.assertEqual(
            repr(validator),
            'validate_list(validator=validate_int(), required=False)',
        )


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

    def test_repr(self):
        validator = validate_set(min_length=1, max_length=100)
        self.assertEqual(
            repr(validator),
            'validate_set(min_length=1, max_length=100)',
        )

        validator = validate_set(validator=validate_int(), required=False)
        self.assertEqual(
            repr(validator),
            'validate_set(validator=validate_int(), required=False)',
        )


class ValidateMappingTestCase(unittest.TestCase):
    def test_basic_valid(self):
        validate_mapping({
            "key1": 1,
            "key2": 2,
        })

    def test_valid_keys(self):
        validate_mapping({
            u"key1": 1,
            u"key2": 2,
        }, key_validator=validate_text())

    def test_invalid_key_type(self):
        with self.assertRaises(TypeError):
            validate_mapping({
                u"key1": 1,
                u"key2": 2,
            }, key_validator=validate_int())

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            validate_mapping({
                u"key1": 1,
                u"key2": 2,
            }, key_validator=validate_text(min_length=20))

    def test_key_validator_positional_argument(self):
        def validator(*args):
            assert len(args) == 1

        validate_mapping({"key": "value"}, key_validator=validator)

    def test_invalid_value_type(self):
        with self.assertRaises(TypeError):
            validate_mapping({
                u"key1": "1",
                u"key2": "2",
            }, value_validator=validate_int())

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            validate_mapping({
                u"key1": 1,
                u"key2": 2,
            }, value_validator=validate_int(max_value=1))

    def test_value_validator_positional_argument(self):
        def validator(*args):
            assert len(args) == 1

        validate_mapping({"key": "value"}, value_validator=validator)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_mapping([
                (u"key1", 1),
                (u"key2", 2),
            ])

    def test_required(self):
        validate_mapping(None, required=False)

        with self.assertRaises(TypeError):
            validate_mapping(None)

    def test_closure(self):
        validator = validate_mapping(key_validator=validate_int())
        validator({1: 2})
        with self.assertRaises(TypeError):
            validator({"1": 1})

    def test_repr(self):
        validator = validate_mapping(
            key_validator=validate_text(), value_validator=validate_int(),
        )
        self.assertEqual(
            repr(validator),
            'validate_mapping('
            'key_validator=validate_text(), value_validator=validate_int()'
            ')',
        )


class ValidateStructureTestCase(unittest.TestCase):
    def test_basic_valid(self):
        validate_structure({'hello': "world"})

    def test_schema_valid(self):
        validator = validate_structure(schema={
            'hello': validate_text(),
            'count': validate_int(),
        })

        validator({'hello': u"world", 'count': 2})

    def test_schema_invalid_value_type(self):
        validator = validate_structure(schema={
            'hello': validate_text(),
            'count': validate_int(),
        })

        with self.assertRaises(TypeError):
            validator({
                'hello': u"world",
                'count': "one hundred",
            })

    def test_schema_invalid_value(self):
        validator = validate_structure(schema={
            'hello': validate_text(),
            'count': validate_int(min_value=0),
        })

        with self.assertRaises(ValueError):
            validator({
                'hello': u"world",
                'count': -1,
            })

    def test_schema_positional_argument(self):
        def validator(*args):
            assert len(args) == 1

        validate_structure({"key": "value"}, schema={"key": validator})

    def test_schema_unexpected_key(self):
        validator = validate_structure(schema={
            'expected': validate_int(),
        })

        with self.assertRaises(ValueError):
            validator({
                'expected': 1,
                'unexpected': 2,
            })

    def test_schema_allow_extra(self):
        validator = validate_structure(schema={
            'expected': validate_int(),
        }, allow_extra=True)

        validator({
            'expected': 1,
            'unexpected': 2,
        })

    def test_repr(self):
        validator = validate_structure(schema={'key': validate_int()})
        self.assertEqual(
            repr(validator),
            'validate_structure(schema={\'key\': validate_int()})',
        )


class ValidateTupleTestCase(unittest.TestCase):
    pass


class ValidateEnumTestCase(unittest.TestCase):
    pass
