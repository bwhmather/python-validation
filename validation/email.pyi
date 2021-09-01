from typing import Union, overload, Callable, Optional, Text

import six

@overload
def validate_email_address(
    value: Text,
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
) -> None: ...

@overload
def validate_email_address(
    value: Optional[Text],
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
) -> Callable[[Optional[Text]], None]: ...

@overload
def validate_email_address(
    *,
    allow_unnormalized: bool=False,
    allow_smtputf8: bool=True,
) -> Callable[[Text], None]: ...
