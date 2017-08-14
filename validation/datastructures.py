import sys

import six

from .core import _validate_int, _validate_bool


_undefined = object()


def _try_contextualize_exception(context):
    """
    Attempts to re-raise a `TypeError` or `ValueError` with a description of
    the context.

    If the original error does not match the expected form, will simply return
    without raising anything.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_type not in (TypeError, ValueError, KeyError):
        # No safe way to extend the message for subclasses.
        return

    # Check that the exception has been properly constructed.  The
    # documentation requires that :exception:`TypeError`s and
    # :exception:`ValueError`s are constructed with a single,
    # string argument, but this is not enforced anywhere.
    if len(exc_value.args) != 1:
        return

    if not isinstance(exc_value.args[0], str):
        return

    message = "{context}:  {message}".format(
        context=context, message=exc_value.args[0],
    )

    six.raise_from(exc_type(message), exc_value)


def _validate_list(
    value, validator=None,
    min_length=None, max_length=None,
    required=True,
):
    if value is None:
        if not required:
            return
        raise TypeError("required value is None")

    if not isinstance(value, list):
        raise TypeError((
            "expected 'list', value is of type {cls!r}"
        ).format(cls=type(value).__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "expected at least {expected} elements, "
            "but list contains only {actual}"
        ).format(expected=min_length, actual=len(value)))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "expected at most {expected} elements, "
            "but list contains {actual}"
        ).format(expected=max_length, actual=len(value)))

    if validator is not None:
        for index, item in enumerate(value):
            try:
                validator(item)
            except (TypeError, ValueError, KeyError):
                _try_contextualize_exception(
                    "invalid item at position {index}".format(index=index),
                )
                raise


def validate_list(
    value=_undefined,
    validator=None,
    min_length=None, max_length=None,
    required=True,
):
    """
    Checks that the supplied value is a valid list.

    :param list value:
        The array to be validated.
    :param func validator:
        A function to be called on each value in the list to check that it is
        valid.
    :param int min_length:
        The minimum acceptable length for the list.  If `None`, the minimum
        length is not checked.
    :param int max_length:
        The maximum acceptable length for the list.  If `None`, the maximum
        length is not checked.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.
     """
    _validate_int(max_length, min_value=0, required=False)
    # The max_value check here is fine.  If max_length is None then there is no
    # cap on the min_length.  We do validate max_length first though.
    _validate_int(
        min_length, min_value=0, max_value=max_length, required=False,
    )
    _validate_bool(required)

    def validate(value):
        _validate_list(
            value, validator=validator,
            min_length=min_length, max_length=max_length,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_set(
    value, validator=None,
    min_length=None, max_length=None,
    required=True,
):
    if value is None:
        if not required:
            return
        raise TypeError("required value is None")

    if not isinstance(value, set):
        raise TypeError((
            "expected 'set', but value is of type {cls!r}"
        ).format(cls=type(value).__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "expected at least {expected} entries, "
            "but set contains only {actual}"
        ).format(expected=min_length, actual=len(value)))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "expected at most {expected} entries, "
            "but set contains {actual}"
        ).format(expected=max_length, actual=len(value)))

    if validator is not None:
        for item in value:
            validator(item)


def validate_set(
    value=_undefined,
    validator=None,
    min_length=None, max_length=None,
    required=True,
):
    """
    Validator to check a set and all entries in it.

    :param set value:
        The set to be validated.
    :param func validator:
        A function to be called on each entry in the set to check that it is
        valid.
    :param int min_length:
        The minimum acceptable number of entries in the set.  If `None`, the
        minimum size is not checked.
    :param int max_length:
        The maximum acceptable number of entries in the set.  If `None`, the
        maximum size is not checked.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.
     """
    _validate_int(max_length, min_value=0, required=False)
    # The max_value check here is fine.  If max_length is None then there is no
    # cap on the min_length.  We do validate max_length first though.
    _validate_int(
        min_length, min_value=0, max_value=max_length, required=False,
    )
    _validate_bool(required)

    def validate(value):
        _validate_set(
            value, validator=validator,
            min_length=min_length, max_length=max_length,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_mapping(
    value,
    key_validator=None, value_validator=None,
    required=True,
):
    if value is None:
        if not required:
            return
        raise TypeError("required value is None")

    if not isinstance(value, dict):
        raise TypeError((
            "expected 'dict', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    for item_key, item_value in value.items():
        if key_validator is not None:
            try:
                key_validator(item_key)
            except (TypeError, ValueError, KeyError):
                _try_contextualize_exception(
                    "invalid key {key!r}".format(key=item_key),
                )
                raise

        if value_validator is not None:
            try:
                value_validator(item_value)
            except (TypeError, ValueError, KeyError):
                _try_contextualize_exception(
                    "invalid value for key {key!r}".format(key=item_key),
                )
                raise


def validate_mapping(
    value=_undefined,
    key_validator=None, value_validator=None,
    required=True,
):
    """
    Validates a dictionary representing a simple mapping from keys of one type
    to values of another.

    :param dict value:
        The value to be validated.
    :param func key_validator:
        Optional function to be call to check each of the keys in the
        dictionary.
    :param func value_validator:
        Optional function to be call to check each of the values in the
        dictionary.
    :param bool required:
        Whether the value can't be `None`. Defaults to `True`.
    """
    _validate_bool(required)

    def validate(value):
        _validate_mapping(
            value,
            key_validator=key_validator,
            value_validator=value_validator,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_structure(
    value,
    schema=None, allow_extra=False,
    required=True,
):
    if value is None:
        if not required:
            return
        raise TypeError("required value is None")

    if not isinstance(value, dict):
        raise TypeError((
            "expected 'dict' but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if schema is not None:
        for key, validator in schema.items():
            if key not in value:
                raise KeyError((
                    "dictionary missing expected key: {key!r}"
                ).format(key=key, dictionary=value))

            try:
                validator(value[key])
            except (TypeError, ValueError, KeyError):
                _try_contextualize_exception(
                    "invalid value for key {key!r}".format(key=key),
                )
                raise

        if not allow_extra and set(schema) != set(value):
            raise ValueError((
                "dictionary contains unexpected keys: {unexpected}"
            ).format(
                unexpected=', '.join(
                    repr(unexpected)
                    for unexpected in set(value) - set(schema)
                )
            ))


def validate_structure(
    value=_undefined,
    schema=None, allow_extra=False,
    required=True,
):
    """
    Validates a structured dictionary, with value types depending on the key,
    checking it against an optional schema.

    The schema should be a dictionary, with keys corresponding to the expected
    keys in `value`, but with the values replaced by functions which will be
    called to with the corresponding value in the input.

    A simple example:

    .. code:: python

        validator = validate_structure(schema={
            'id': validate_key(kind='Model'),
            'count': validate_int(min=0),
        })
        validator({'id': self.key, 'count': self.count})

    :param dict value:
        The value to be validated.
    :param dict schema:
        The schema against which the value should be checked.
    :param bool allow_extra:
        Set to `True` to ignore extra keys.
    :param bool required:
        Whether the value can't be `None`. Defaults to True.
    """
    _validate_structure(schema, schema=None, required=False)
    _validate_bool(allow_extra)
    _validate_bool(required)

    # Make a copy of the schema to make sure it won't be mutated under us.
    if schema is not None:
        schema = dict(schema)

    def validate(value):
        _validate_structure(
            value,
            schema=schema, allow_extra=allow_extra,
            required=required,
        )

    if value is not _undefined:
        validate(value)
    else:
        return validate


def validate_tuple(
    value=_undefined,
    schema=None,
    required=True,
):
    raise NotImplementedError()


def validate_enum(
    value=_undefined,
    kind=None,
    required=True,
):
    raise NotImplementedError()
