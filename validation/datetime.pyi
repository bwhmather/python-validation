from typing import overload, Callable
from datetime import date, datetime

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
