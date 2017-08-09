from typing import Callable, List, Set, Tuple, Dict, Type, TypeVar, overload
from enum import Enum
from datetime import date, datetime


T = TypeVar('T')


@overload
def validate_list(
    value: List[T],
    *, min_length: int=None, max_length: int=None,
    validator: Callable[[T], None],
    required: bool=True,
) -> None:
    ...


@overload
def validate_list(
    *, min_length: int=None, max_length: int=None,
    validator: Callable[[T], None],
    required: bool=True,
) -> Callable[[List[T]], None]:
    ...


@overload
def validate_set(
    value: Set[T],
    *, min_length: int=None, max_length: int=None,
    validator: Callable[[T], None],
    required: bool=True,
) -> None:
    ...


@overload
def validate_set(
    *, min_length: int=None, max_length: int=None,
    validator: Callable[[T], None],
    required: bool=True,
) -> Callable[[Set[T]], None]:
    ...


@overload
def validate_tuple(
    value: Tuple,
    *, required: bool=False,
    schema: Tuple=None,
) -> None:
    ...


@overload
def validate_tuple(
    *, required: bool=False,
    schema: Tuple=None,
) -> Callable[[Tuple], None]:
    ...


@overload
def validate_dict(
    value: Dict,
    *, allow_extra: bool=False,
    schema: Dict=None,
    required: bool=False,
) -> None:
    ...


@overload
def validate_dict(
    *, allow_extra: bool=False,
    schema: Dict=None,
    required: bool=False,
) -> Callable[[Tuple], None]:
    ...


E = TypeVar('E', bound=Enum)


@overload
def validate_enum(
    value: E,
    *, kind: Type[E],
    required: bool=True,
) -> None:
    ...


@overload
def validate_enum(
    *, kind: Type[E],
    required: bool=True,
) -> Callable[[E], None]:
    ...
