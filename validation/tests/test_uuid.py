import unittest
import uuid

from validation import validate_uuid


class ValidateUUIDTestCase(unittest.TestCase):
    def test_uuid1_valid(self):
        validate_uuid(uuid.uuid1())

    def test_uuid1_expected_valid(self):
        validate_uuid(uuid.uuid1(), version=1)

    def test_uuid1_expected_invalid(self):
        with self.assertRaises(ValueError):
            validate_uuid(uuid.uuid4(), version=1)

    def test_uuid3_valid(self):
        validate_uuid(uuid.uuid3(uuid.uuid4(), "name"))

    def test_uuid3_expected_valid(self):
        validate_uuid(uuid.uuid3(uuid.uuid4(), "name"), version=3)

    def test_uuid3_expected_invalid(self):
        with self.assertRaises(ValueError):
            validate_uuid(uuid.uuid4(), version=3)

    def test_uuid4_valid(self):
        validate_uuid(uuid.uuid4())

    def test_uuid5_valid(self):
        validate_uuid(uuid.uuid5(uuid.uuid4(), "name"))

    def test_rfc4122_valid(self):
        validate_uuid(uuid.uuid4(), variant=uuid.RFC_4122)

    def test_microsoft_invalid(self):
        with self.assertRaises(ValueError):
            validate_uuid(uuid.uuid4(), variant=uuid.RESERVED_MICROSOFT)

    def test_incompatible_variant_version(self):
        with self.assertRaises(ValueError):
            validate_uuid(variant=uuid.RESERVED_MICROSOFT, version=4)

    def test_not_required(self):
        validate_uuid(None, required=False)

    def test_required(self):
        with self.assertRaises(TypeError):
            validate_uuid(None)

    def test_repr_required_false(self):
        validator = validate_uuid(required=False)
        self.assertEqual(
            repr(validator),
            'validate_uuid(required=False)',
        )

    def test_repr_full(self):
        validator = validate_uuid(variant=uuid.RFC_4122, version=3)
        self.assertEqual(
            repr(validator),
            'validate_uuid(variant=uuid.RFC_4122, version=3)',
        )
