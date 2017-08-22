from typing import Union, overload, Callable, Pattern
from datetime import date, datetime


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
    required: bool=True,
) -> None:
    ...


@overload
def validate_float(
    *, min_value: float=None, max_value: float=None,
    required: bool=True,
) -> Callable[[float], None]:
    ...


@overload
def validate_bool(
    value: bool,
    *, required: bool=True,
) -> None:
    ...


@overload
def validate_bool(
    *, required: bool=True,
) -> Callable[[bool], None]:
    ...


@overload
def validate_text(
    value: str,
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
    required: bool=True,
) -> None:
    ...


@overload
def validate_text(
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
    required: bool=True,
) -> Callable[[str], None]:
    ...


@overload
def validate_bytes(
    value: bytes,
    *, min_length: int=None, max_length: int=None,
    required: bool=True,
) -> None:
    ...


@overload
def validate_bytes(
    *, min_length: int=None, max_length: int=None,
    required: bool=True,
) -> Callable[[bytes], None]:
    ...


@overload
def validate_date(
    value: date,
    *, required: bool=False,
) -> None:
    ...


@overload
def validate_date(
    *, required: bool=False,
) -> Callable[[date], None]:
    ...


@overload
def validate_datetime(
    value: datetime,
    *, required: bool=False,
) -> None:
    ...


@overload
def validate_datetime(
    *, required: bool=False,
) -> Callable[[datetime], None]:
    ...
