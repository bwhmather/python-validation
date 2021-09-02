from __future__ import absolute_import

import uuid

from .core import _validate_bool
from .number import _validate_int
from .common import make_optional_argument_default


_undefined = make_optional_argument_default()


def _variant_to_string(variant):
    return {
        uuid.RESERVED_NCS: "RESERVED_NCS",
        uuid.RFC_4122: "RFC_4122",
        uuid.RESERVED_MICROSOFT: "RESERVED_MICROSOFT",
        uuid.RESERVED_FUTURE: "RESERVED_FUTURE",
    }.get(variant, "unknown")


def _validate_uuid(
    value,
    variant,
    version,
    required
):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, uuid.UUID):
        raise TypeError((
            "expected uuid, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if variant is not None and value.variant != variant:
        raise ValueError((
            "expected {expected} variant, but uuid variant is {actual}"
        ).format(
            expected=_variant_to_string(variant),
            actual=_variant_to_string(value.variant)
        ))

    if version is not None and value.version != version:
        raise ValueError((
            "expected UUID{expected}, but received UUID{actual}"
        ).format(expected=version, actual=version))


class _uuid_validator(object):
    def __init__(
        self,
        variant,
        version,
        required
    ):
        if variant is not None and variant not in (
            uuid.RESERVED_NCS,
            uuid.RFC_4122,
            uuid.RESERVED_MICROSOFT,
            uuid.RESERVED_FUTURE,
        ):
            raise ValueError("unknown variant")
        self.__variant = variant

        _validate_int(version, required=False)
        if version is not None:
            if version not in (1, 3, 4, 5):
                raise ValueError(
                    "unknown UUID version: {version}".format(version=version)
                )

            if variant is None:
                variant = uuid.RFC_4122

            if variant != uuid.RFC_4122:
                raise ValueError((
                    "version is specified, but variant is {variant}"
                ).format(variant=_variant_to_string(variant)))
        self.__version = version

        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_uuid(
            value,
            variant=self.__variant,
            version=self.__version,
            required=self.__required
        )

    def __repr__(self):
        args = []
        if self.__variant is not None:
            args.append('variant=uuid.{variant}'.format(
                variant=_variant_to_string(self.__variant),
            ))

        if self.__version is not None:
            args.append('version={version!r}'.format(
                version=self.__version,
            ))

        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_uuid({args})'.format(args=', '.join(args))


def validate_uuid(
    value=_undefined,
    variant=None,
    version=None,
    required=True,
):
    """
    Checks that the target value is a valid UUID.

    Parameters can be used to narrow down exactly what sort of UUID is
    expected.

    .. code:: python

        def do_the_thing(identifier):
            validate_uuid(
                identifier,
                variant=uuid.RFC_4122,
                version=3,
            )

            # Do something
            ...

    :param unicode value:
        The uuid to be validated.
    :param int variant:
        The UUID variant determines the internal layout of the UUID. This must
        be one of `RESERVED_NCS`, `RFC_4122`, `RESERVED_MICROSOFT`, or
        `RESERVED_FUTURE` from the `uuid` module.
    :param int version:
        Can be 1, 3, 4, or 5.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.

    :raises TypeError:
        If the value is not a unicode string , or if it was marked as
        `required` but `None` was passed in.
    :raises ValueError:
        If the value was longer or shorter than expected, or did not match
        the pattern.
    """
    validate = _uuid_validator(
        variant=variant,
        version=version,
        required=required,
    )

    if value is not _undefined:
        validate(value)
    else:
        return validate
