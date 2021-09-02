from typing import Union, overload, Callable, Pattern, Optional, Text
import six


@overload
def validate_text(
    value: Text,
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
) -> None:
    ...


@overload
def validate_text(
    value: Optional[Text],
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
    required: bool,
) -> None:
    ...


@overload
def validate_text(
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
) -> Callable[[Text], None]:
    ...


@overload
def validate_text(
    *, min_length: int=None, max_length: int=None,
    pattern: Union[str, Pattern]=None,
    required: bool,
) -> Callable[[Optional[Text]], None]:
    ...


@overload
def validate_bytes(
    value: bytes,
    *, min_length: int=None, max_length: int=None,
) -> None:
    ...


@overload
def validate_bytes(
    value: Optional[bytes],
    *, min_length: int=None, max_length: int=None,
    required: bool,
) -> None:
    ...


@overload
def validate_bytes(
    *, min_length: int=None, max_length: int=None,
) -> Callable[[bytes], None]:
    ...


@overload
def validate_bytes(
    *, min_length: int=None, max_length: int=None,
    required: bool,
) -> Callable[[Optional[bytes]], None]:
    ...
