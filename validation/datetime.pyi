from typing import overload, Callable, Optional
from datetime import date, datetime, timedelta


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
def validate_datetime(value: datetime) -> None:
    ...


@overload
def validate_datetime(
    value: Optional[datetime],
    *, required: bool,
) -> None:
    ...


@overload
def validate_datetime() -> Callable[[datetime], None]:
    ...


@overload
def validate_datetime(
    *, required: bool,
) -> Callable[[Optional[datetime]], None]:
    ...


@overload
def validate_timedelta(
    value: timedelta,
    *,
    max_value: Optional[timedelta] = None,
    min_value: Optional[timedelta] = None,
) -> None:
    ...

@overload
def validate_timedelta(
    value: Optional[timedelta],
    *,
    max_value: Optional[timedelta] = None,
    min_value: Optional[timedelta] = None,
    required: bool,
) -> None:
    ...


@overload
def validate_timedelta(
    *,
    max_value: Optional[timedelta] = None,
    min_value: Optional[timedelta] = None,
) -> Callable[[timedelta], None]:
    ...


@overload
def validate_timedelta(
    *,
    max_value: Optional[timedelta] = None,
    min_value: Optional[timedelta] = None,
    required: bool,
) -> Callable[[Optional[timedelta]], None]:
    ...
