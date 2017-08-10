import six

from .base import validator


_undefined = object()


def _validate_int(value, min_value=None, max_value=None, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.integer_types):
        raise TypeError((
            "expected int, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if min_value is not None and value < min_value:
        raise ValueError((
            "{value!r} is less than minimum acceptable {min!r}"
        ).format(value=value, min=min_value))

    if max_value is not None and value > max_value:
        raise ValueError((
            "{value!r} is greater than maximum acceptable {max!r}"
        ).format(value=value, max=max_value))


def validate_int(
    value=_undefined,
    min_value=None, max_value=None,
    required=True,
):
    """
    Validator for integer values.

    :param int value:
        The number to be validated.
    :param int min_value:
        The minimum acceptable value for the number.
    :param int max_value:
        The maximum acceptable value for the number.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.
    """
    _validate_int(min_value, required=False)
    _validate_int(max_value, min_value=min_value, required=False)

    def validate(value):
        _validate_int(
            value,
            min_value=min_value, max_value=max_value,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


@validator
def validate_float(value, min_value=None, max_value=None):
    raise NotImplementedError()


def _validate_bool(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, bool):
        raise TypeError((
            "expected bool, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))


def validate_bool(value=_undefined, required=True):
    """
    Validator for boolean values.

    :param value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to True.
    """
    _validate_bool(required)

    def validate(value):
        _validate_bool(value, required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate


@validator
def validate_text(value, min_length=None, max_length=None):
    raise NotImplementedError()


@validator
def validate_bytes(value, min_length=None, max_length=None):
    raise NotImplementedError()


@validator
def validate_date(value):
    raise NotImplementedError()


@validator
def validate_datetime(value):
    raise NotImplementedError()
