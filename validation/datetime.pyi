from typing import overload, Callable, Optional
from datetime import date, datetime


@overload
def validate_date(value: date) -> None:
    ...


@overload
def validate_date(
    value: Optional[date],
    *, required: bool,
) -> None:
    ...


@overload
def validate_date() -> Callable[[date], None]:
    ...


@overload
def validate_date(
    *, required: bool,
) -> Callable[[Optional[date]], None]:
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
