from __future__ import absolute_import

from datetime import date, datetime, timedelta

from .core import _validate_bool
from .common import make_optional_argument_default


_undefined = make_optional_argument_default()


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
            "expected 'date', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))


class _date_validator(object):
    def __init__(self, required):
        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_date(value, required=self.__required)

    def __repr__(self):
        args = []
        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_date({args})'.format(args=', '.join(args))


def validate_date(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.date` value.

    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.

    :raises TypeError:
        If the value is not a date, or if it was marked as `required` but
        None was passed in.
    """
    validate = _date_validator(required=required)

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
            "expected 'datetime', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if value.tzinfo is None:
        raise ValueError((
            "datetime object is missing timezone"
        ))


class _datetime_validator(object):
    def __init__(self, required):
        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_datetime(value, required=self.__required)

    def __repr__(self):
        args = []
        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_datetime({args})'.format(args=', '.join(args))


def validate_datetime(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.datetime` value.

    The value must have a valid timezone to be accepted.  Naive `datetime`
    objects are not allowed.

    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.

    :raises TypeError:
        If the value is not a datetime, or if it was marked as `required` but
        None was passed in.
    :raises ValueError:
        If the value does not have a valid timezone.
    """
    validate = _datetime_validator(required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_timedelta(value, min_value=None, max_value=None, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, timedelta):
        raise TypeError((
            "expected 'timedelta', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if min_value is not None and value < min_value:
        raise ValueError((
            "expected value less than {min}, but got {value}"
        ).format(value=value, min=min_value))

    if max_value is not None and value > max_value:
        raise ValueError((
            "expected value greater than {max}, but got {value}"
        ).format(value=value, max=max_value))


class _timedelta_validator(object):
    def __init__(self, min_value, max_value, required):
        _validate_timedelta(min_value, required=False)
        _validate_timedelta(max_value, required=False)
        if (
            min_value is not None
            and max_value is not None
            and min_value > max_value
        ):
            raise ValueError("minimum value greater than max value")
        _validate_bool(required)
        self.__min_value = min_value
        self.__max_value = max_value
        self.__required = required

    def __call__(self, value):
        _validate_timedelta(value, required=self.__required)

    def __repr__(self):
        args = []
        if self.__min_value is not None:
            args.append('min_value={min_value!r}'.format(
                min_value=self.__min_value,
            ))

        if self.__max_value is not None:
            args.append('min_value={max_value!r}'.format(
                max_value=self.__max_value,
            ))

        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_timedelta({args})'.format(args=', '.join(args))


def validate_timedelta(
    value=_undefined,
    min_value=None,
    max_value=None,
    required=True
):
    """
    Checks that the value is a valid :class:`datetime.timedelta` value.

    The value must have a valid timezone to be accepted.  Naive `timedelta`
    objects are not allowed.

    :param datetime.timedelta value:
        The value to be validated.
    :param datetime.timedelta min_value:
        The minimum acceptable value for the number.
    :param datetime.timedelta max_value:
        The maximum acceptable value for the number.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.

    :raises TypeError:
        If the value is not a timedelta, or if it was marked as `required` but
        None was passed in.
    :raises ValueError:
        If the value is not within bounds.
    """
    validate = _timedelta_validator(
        min_value=min_value, max_value=max_value, required=required
    )

    if value is not _undefined:
        validate(value)
    else:
        return validate
