import functools


_undefined = object()


def validator(f):
    @functools.wraps(f)
    def wrapper(value=_undefined, **kwargs):
        required = kwargs.pop('required', True)

        def validate(value):
            if value is None:
                if required:
                    raise TypeError()
                return
            f(value, **kwargs)

        if value is not _undefined:
            validate(value)
        else:
            return validate

    return wrapper
