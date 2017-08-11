from .core import _validate_int, _validate_bool


_undefined = object()


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
            "expected list, got {cls!r}"
        ).format(cls=type(value).__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "expected at least {expected} elements, "
            "but list is of length {actual}"
        ).format(expected=min_length, actual=len(value)))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "expected at most {expected} elements, "
            "but list is of length {actual}"
        ).format(expected=max_length, actual=len(value)))

    if validator is not None:
        for item in value:
            validator(item)


def validate_list(
    value=_undefined,
    validator=None,
    min_length=None, max_length=None,
    required=True,
):
    """
    Validator to check a list and all of its contents.

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
            "expected set, got {cls!r}"
        ).format(cls=type(value).__name__))

    if min_length is not None and len(value) < min_length:
        raise ValueError((
            "expected at least {expected} elements, "
            "but set contains only {actual}"
        ).format(expected=min_length, actual=len(value)))

    if max_length is not None and len(value) > max_length:
        raise ValueError((
            "expected at most {expected} elements, "
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


def validate_tuple(
    value=_undefined,
    schema=None,
    required=True,
):
    raise NotImplementedError()


def validate_dict(
    value=_undefined,
    schema=None, allow_extra=False, default=None,
    required=True,
):
    raise NotImplementedError()


def validate_enum(
    value=_undefined,
    kind=None,
    required=True,
):
    raise NotImplementedError()
