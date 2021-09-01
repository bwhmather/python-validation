from typing import Union, overload, Callable, Optional

import six

@overload
def validate_email_address(
    value: six.text_type,
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
) -> None: ...

@overload
def validate_email_address(
    value: Optional[six.text_type],
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
    required: bool,
) -> None: ...

@overload
def validate_email_address(
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
    required: bool,
) -> Callable[[Optional[six.text_type]], None]: ...

@overload
def validate_email_address(
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
) -> Callable[[six.text_type], None]: ...
