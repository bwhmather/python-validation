from typing import overload, Callable


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
