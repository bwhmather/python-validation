import re
from datetime import date, datetime

import six


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


def validate_float(
    value=_undefined,
    min_value=None, max_value=None,
    required=True,
):
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


def _validate_text(
    value,
    min_length=None, max_length=None,
    pattern=None,
    required=True,
):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.text_type):
        raise TypeError((
            "expected unicode string, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "{length} is shorter than minimum acceptable {min}"
        ).format(length=len(value), min=min_length))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "{length} is longer than maximum acceptable {max}"
        ).format(length=len(value), max=max_length))

    if pattern is not None:
        # Unfortunately `fullmatch` is not available in python2.
        match = pattern.match(value)

        if not (
            match is not None and
            match.start() == 0 and
            match.end() == len(value)
        ):
            raise ValueError(
                "string did not match pattern"
            )


def validate_text(
    value=_undefined,
    min_length=None, max_length=None,
    pattern=None,
    required=True,
):
    """
    Validator for human readable string values.

    :param unicode value:
        The string to be validated.
    :param int min_length:
        The minimum length of the string.
    :param int max_length:
        The maximum acceptable length for the string.  By default, the length
        is not checked.
    :param str|re.SRE_Pattern pattern:
        Regular expression to check the value against.
    :param bool required:
        Whether the value can be `None`.  Defaults to True.
    """
    _validate_int(max_length, min_value=0, required=False)
    # The max_value check here is fine.  If max_length is None then there is no
    # cap on the min_length.  We do validate max_length first though.
    _validate_int(
        min_length, min_value=0, max_value=max_length, required=False,
    )
    _validate_bool(required)

    if pattern is not None:
        # Note that we are a little more permissive about non-unicode patterns
        # in python2 than we are about non-unicode arguments.  Users will
        # probably written the pattern argument inline.
        if isinstance(pattern, six.string_types):
            pattern = re.compile(pattern)

        # `re` does not expose a class for regular expression objects, so it
        # is not possible to do any validation here.

    def validate(value):
        _validate_text(
            value,
            min_length=min_length, max_length=max_length,
            pattern=pattern,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_bytes(value, min_length, max_length, required):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.binary_type):
        raise TypeError((
            "expected byte string, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "{length} is shorter than minimum acceptable {min}"
        ).format(length=len(value), min=min_length))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "{length} is longer than maximum acceptable {max}"
        ).format(length=len(value), max=max_length))


def validate_bytes(
    value=_undefined,
    min_length=None, max_length=None,
    required=True,
):
    """
    Validator for bytestring values.

    Should not be used for validating human readable strings,  Please use
    :function:`validate_string` instead.

    :param bytes value:
        The string to be validated.
    :param int min_length:
        The minimum length of the string.
    :param int max_length:
        The maximum acceptable length for the string.  By default, the length
        is not checked.
    :param bool required:
        Whether the value can be `None`.  Defaults to True.
    """
    _validate_int(max_length, min_value=0, required=False)
    # The max_value check here is fine.  If max_length is None then there is no
    # cap on the min_length.  We do validate max_length first though.
    _validate_int(
        min_length, min_value=0, max_value=max_length, required=False,
    )
    _validate_bool(required)

    def validate(value):
        _validate_bytes(
            value,
            min_length=min_length, max_length=max_length,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_date(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    # :class:`datetime` is a subclass of :class:`date`, but we really don't
    # want to accept it as it behaves very differently (timezones, leap
    # seconds, etc) and is usually presented in a very different way.
    if not isinstance(value, date) or isinstance(value, datetime):
        raise TypeError((
            "expected date, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))


def validate_date(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.date` value.

    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to True.
    """
    def validate(value):
        _validate_date(value, required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_datetime(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, datetime):
        raise TypeError((
            "expected datetime, but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if value.tzinfo is None:
        raise ValueError((
            "datetime object is missing timezone"
        ))


def validate_datetime(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.datetime` value.

    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to True.
    """
    def validate(value):
        _validate_datetime(value, required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate
