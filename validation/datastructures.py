_undefined = object()


def validate_list(
    value=_undefined,
    validator=None,
    min_length=None, max_length=None,
    required=True,
):
    raise NotImplementedError()


def validate_set(
    value=_undefined,
    validator=None,
    min_length=None, max_length=None,
    required=True,
):
    raise NotImplementedError()


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
