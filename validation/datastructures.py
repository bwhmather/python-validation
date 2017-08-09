from .base import validator


@validator
def validate_list(value, validator=None, min_length=None, max_length=None):
    raise NotImplementedError()


@validator
def validate_set(value, validator=None, min_length=None, max_length=None):
    raise NotImplementedError()


@validator
def validate_tuple(value, schema=None):
    raise NotImplementedError()


@validator
def validate_dict(value, schema=None, allow_extra=False, default=None):
    raise NotImplementedError()


@validator
def validate_enum(value, kind):
    raise NotImplementedError()
