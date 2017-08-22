from typing import overload, Callable


@overload
def validate_int(
    value: int,
    *, min_value: int=None, max_value: int=None,
    required: bool=True,
) -> None:
    ...


@overload
def validate_int(
    *, min_value: int=None, max_value: int=None,
    required: bool=True,
) -> Callable[[int], None]:
    ...


@overload
def validate_float(
    value: float,
    *, min_value: float=None, max_value: float=None,
    allow_infinite: bool=False, allow_nan: bool=False,
    required: bool=True,
) -> None:
    ...


@overload
def validate_float(
    *, min_value: float=None, max_value: float=None,
    allow_infinite: bool=False, allow_nan: bool=False,
    required: bool=True,
) -> Callable[[float], None]:
    ...
