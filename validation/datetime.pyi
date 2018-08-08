from typing import overload, Callable
from datetime import date, datetime


@overload
def validate_date(
    value: date,
    *, required: bool=True,
) -> None:
    ...


@overload
def validate_date(
    *, required: bool=True,
) -> Callable[[date], None]:
    ...


@overload
def validate_datetime(
    value: datetime,
    *, required: bool=True,
) -> None:
    ...


@overload
def validate_datetime(
    *, required: bool=True,
) -> Callable[[datetime], None]:
    ...
