from typing import Union, overload, Callable, Pattern, Optional
from uuid import UUID
import six


@overload
def validate_uuid(
    value: UUID,
    *,
    variant: Optional[str] = None,
    version: Optional[int] = None,
) -> None:
    ...


@overload
def validate_uuid(
    value: Optional[UUID],
    *,
    variant: Optional[str] = None,
    version: Optional[int] = None,
    required: bool,
) -> None:
    ...


@overload
def validate_uuid(
    *,
    variant: Optional[str] = None,
    version: Optional[int] = None,
) -> Callable[[UUID], None]:
    ...


@overload
def validate_uuid(
    *,
    variant: Optional[str] = None,
    version: Optional[int] = None,
    required: bool,
) -> Callable[[Optional[UUID]], None]:
    ...

