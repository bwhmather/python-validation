.. design:

======
Design
======

Validators are intended as an easy way to start rolling out type-checking in an existing codebase.

Validators only raise built in exceptions
=========================================

This library does not introduce any custom exception types.
It instead limits itself to the exception types defined in the standard
library.
This in practice means ``TypeError``, ``ValueError`` or, on rare occasions,
``KeyError``.


There are two main reasons for this:

- Using built-in errors means that other libraries can use this package to
  validate arguments passed to their public API without catching, wrapping and
  re-raising the exceptions it raises, or leaking implementation details.

- Using built-in errors makes it much easier to mix custom validation with
  validation using the validation functions.
  There is no pressure to add a new class for every error condition, and no
  need to fit custom exceptions into the validation library exception
  hierarchy.

The main reason to consider introducing custom exceptions is that it would
allow calling code to behave differently depending on what issues were
detected.
For the intended application of this library, to serve as a runtime
type-checker for function arguments, I don't think that this would be useful.


Exceptions raised by validators will contain only a message
===========================================================

The reasons here are similar to the reasons for using built-in exceptions:

- It's much easier to keep simple messages consistent.
  This is particularly important as we want to encourage mixing with custom
  validation code.

- It is expected that the exceptions will be interpreted by a developer, not by
  by the calling logic.
  There is no requirement for machine readable information.

- This restriction, along with the restriction on exception types, makes it
  easy to add context information to exceptions thrown from within the
  data-structure validation functions.

There is also the simple reason that the standard library documentation demands
it.


Validators do not return a value
================================

If a value is not in the expected form going in then it is an error.

Callers are likely to forget to use the fixed return value rather than the
invalid original.


Validators will never modify the values that they are passed
============================================================
This is for the same reason that validators do not return values, but in this case the justification is stronger.
This is the reason that we do not provide generic validators for iterables: an iterator is a valid iterable, but would be rendered useless by the process of being validated.
