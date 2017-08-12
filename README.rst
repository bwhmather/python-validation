Python Validation
=================

|build-status| |coverage|

A python library for runtime type checking and validation of python values.

Intended as a stepping stone to static typing.


Usage
-----

All validators are functions which take a single value to check as their
first argument, check its type and that it meets some preconditions, and raises
an exception if it finds something wrong.

.. code:: python

    >>> validation.validate_int(1)
    >>> validation.validate_int(1.5)
    Traceback (most recent call last):
        ...
    TypeError: expected 'int', but value is of type 'float'
    >>> validation.validate_int(-1, min_value=0)
    Traceback (most recent call last):
        ...
    ValueError: expected value greater than 0, but got -1

If the first argument is missing, validators will return a closure that can be
called later to check a value.

.. code:: python

    >>> validator = validation.validate_int(min_value=0)
    >>> validator(-1)
    Traceback (most recent call last):
        ...
    ValueError: expected value greater than 0, but got -1

This is important when using the datastructure validators.
Datastructure validators usually accept as an argument a function to be applied
to each of the values they contain.

.. code:: python

    >>> value = [1, -2]
    >>> validate_list(value, validator=lambda v: validate_int(v, min_value=0))
    Traceback (most recent call last):
        ...
    ValueError: invalid item at position 1: expected value greater than 0 but got -1

This can be expressed more succinctly as:

.. code:: python

    >>> value = [1, -2]
    >>> validate_list(value, validator=validate_int(min_value=0))
    Traceback (most recent call last):
        ...
    ValueError: invalid item at position 1: expected value greater than 0 but got -1


Using the datastructure validators with closures.

Validating iterables.  `list` then `validate_list`, or validate in loop.

This library provides a shorthand for performing simple checks on single
variables.
It does not prevent you from writing more checks in normal python!
As an example, to validate two mutually exclusive arguments:

.. code:: python

    def do_something(arg_a=None, arg_b=None):
        validation.validate_text(arg_a, required=False)
        validation.validate_text(arg_b, required=False)

        if arg_a is None == arg_b is None:
            raise TypeError('arg_a and arg_b are mutually exclusive')

        ...


Creating new validators.

Packaging new validators into a library.


Tips
~~~~

Avoid writing wrappers that hide details your code depends on.

Catch validation errors at the top level.

Alternate validation and assignment to make it clear when validation is missing


Installation
------------

Recommended method is to use the version from `pypi`_:

.. code:: bash

    $ pip install validation

Please note that this library only supports python version 2.7, and versions 3.4 and later.


Versioning
----------

This library strictly follows the `semantic versioning scheme <http://semver.org>`_.
Due to the libraries limited scope we can be fairly explicit about what changes can be expected in a release.

Changes that will require a major version bump:
  - Removing validation functions.
  - Removing or changing the meaning of arguments to validation functions.
  - Increasing the strictness of any existing validation function.  If a value
    passes validation by an older version with the same major version, it will
    pass validation with a newer version.
  - Introducing new external dependencies.
  - Anything else that would be expected to break existing users of the library.

Changes that will require a minor version bump:
  - Adding new validation functions.
  - Adding new arguments to existing validation functions.
  - Relaxing the strictness of any existing validation function.
  - Any other changes that users of the library could use that would prevent
    their code from working with an older version.

Changes that will require only a patch version bump:
  - Bug-fixes that do not affect the expected behaviour.
  - Documentation improvements.
  - Re-releases to fix packaging issues.
  - Changes to exception messages.

Libraries should specify a minimum minor version and maximum major version.
Applications should do likewise but are encouraged to pin a particular version
for releases.


Design
------

Validators are intended as an easy way to start rolling out type-checking in an existing codebase.

It is expected that if validation of a value fails, the error will propagate thought.
A script encountering a validation error should exit with a stack-trace, an http server should return a 500 error


To recover from specific errors reimplement the check explicitly in python.

Error messages are developer focused, and will usually indicate developer mistakes.
They are not intended for directly handling user input.

Requirements:

- Exceptions raised by validators should make sense when they are propagated
  by the calling function.

- Exceptions should contain enough information to immediately identify
  exactly what is wrong with a value if the value can be seen.

- Exceptions should contain enough information to make a good guess at what
  is wrong with a value if the value is no longer available.


Non-requirements:

- Exceptions do not need to contain any information that would allow the
  program to distinguish between errors.

- Validators should not expect to be run on serialized data.


Accordingly we have made some decisions.


Validators only raise built in exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This library does not introduce any custom exception types.
It instead limits itself to the exception types defined in the standard
library.
This in practice means `TypeError`, `ValueError` or, on rare occasions,
`KeyError`.


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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The reasons here are similar to the reasons for using built-in exceptions:

- It's much easier to keep simple messages consistent.
  This is particularly important as we want to encourage mixing with custom
  validation code.

- It is expected that the exceptions will be interpreted by a developer, not by
  by the calling logic.
  There is no requirement for machine readable information.

- This restriction, along with the restriction on exception types, makes it
  easy to add context information to exceptions thrown from within the data-
  structure validation functions.

There is also the simple reason that the standard library documentation demands
it.


Validators do not return a value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if a value is not in the expected form going in then it is an error.
This keeps the API simple, and reduces the temptation


Validators will never modify the values that they are passed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is for the same reason that validators do not return values, but in this case the justification is stronger.
This is the reason that we do not provide generic validators for iterables: an iterator is a valid iterable, but would be rendered useless by the process of being validated.


Validators prioritise performance over comprehensiveness
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
They should never be worse than linear, in time or space, in the size of their input.
More complex validation should not be performed unless requested specifically.
This again comes down to the intended use of the library as a stand-in for a compile time type-checker.



Validator closures should not be usefully introspectable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This makes is much easier for custom functions to be used in place of
validators from this library.




Usability

Checks should pass or fail predictably.
Given the same input, a validator should always behave in the same way.
Given similar input, a validator should also behave similarly.
It would be unacceptable, for example, for the list validator to validate only the first ten elements.


It should be easy to add new validators
validators are just a closure.




All validators should be exposed in a flat namespace.


Validators for datatypes from other libraries should not look out of place.
This is very much a TODO.
Need a convention for naming extension libraries.
Should consider namespace modules and setuptools hooks, but only as a last resort.


Validators do not attempt to cover every possible check.
They provide a succinct way to express the most obvious checks easily.
Users should be prepared to write python for more complex use cases.



Guidelines
----------

- All validators should have complete type annotations.
- `min_value` and `max_value`
- `min_length` and `max_length`
- Exception messages should contain the `repr` of the value that failed.
- Validators should not call other validators

Links
-----

- Source code: https://github.com/JOIVY/validation
- Issue tracker: https://github.com/JOIVY/validation/issues
- Continuous integration: https://travis-ci.org/JOIVY/validation
- PyPI: https://pypi.python.org/pypi/validation


License
-------

The project is made available under the terms of the Apache 2.0 license.  See `LICENSE`_ for details.



.. |build-status| image:: https://travis-ci.org/JOIVY/validation/g.png?branch=develop
    :target: https://travis-ci.org/JOIVY/validation/g
    :alt: Build Status
.. |coverage| image:: https://coveralls.io/repos/JOIVY/validation/g/badge.png?branch=develop
    :target: https://coveralls.io/r/JOIVY/validation/g?branch=develop
    :alt: Coverage
.. _pypi: https://pypi.python.org/pypi/validation
.. _LICENSE: ./LICENSE
