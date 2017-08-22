from typing import Union, overload, Callable, Pattern
import six


@overload
def validate_text(
    value: six.text_type,
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
) -> Callable[[six.text_type], None]:
    ...


@overload
def validate_bytes(
    value: six.binary_type,
    *, min_length: int=None, max_length: int=None,
    required: bool=True,
) -> None:
    ...


@overload
def validate_bytes(
    *, min_length: int=None, max_length: int=None,
    required: bool=True,
) -> Callable[[six.binary_type], None]:
    ...
