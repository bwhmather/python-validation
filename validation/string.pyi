from typing import Union, overload, Callable, Pattern


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
