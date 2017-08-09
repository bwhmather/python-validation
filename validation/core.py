from .base import validator


@validator
def validate_int(value, min_value=None, max_value=None):
    raise NotImplementedError()


@validator
def validate_float(value, min_value=None, max_value=None):
    raise NotImplementedError()


@validator
def validate_bool(value):
    raise NotImplementedError()


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
