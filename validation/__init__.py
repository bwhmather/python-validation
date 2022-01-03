
from .core import (
    validate_bool,
)

from .number import (
    validate_int, validate_float,
)

from .string import (
    validate_text, validate_bytes,
)

from .datetime import (
    validate_date, validate_datetime,
)

from .datastructure import (
    validate_list, validate_set,
    validate_mapping, validate_structure,
    validate_tuple,
)

from .uuid import validate_uuid

try:
    from .email import validate_email_address
except ImportError:
    # `validate_email_address` is only available if the `idna` package is
    # installed.  Depend on `validation[email]` to pull in the right version.
    pass

__all__ = [
    'validate_int', 'validate_float', 'validate_bool',
    'validate_text', 'validate_bytes',
    'validate_date', 'validate_datetime',
    'validate_list', 'validate_set',
    'validate_mapping', 'validate_structure',
    'validate_tuple', 'validate_uuid',
    'validate_email_address',
]
