Python Validation
=================

|build-status|

.. |build-status| image:: https://github.com/bwhmather/python-validation/actions/workflows/ci.yaml/badge.svg?branch=develop
    :target: https://github.com/bwhmather/python-validation/actions/workflows/ci.yaml
    :alt: Build Status

.. begin-docs

A simple Python library containing functions that check Python values.
It is intended to make it easy to verify commonly expected pre-conditions on
arguments to functions.

Originally developed and open-sourced at `Joivy Ltd <https://joivy.com>`_.


Installation
------------
.. begin-installation

The ``validation`` library is available on `PyPI <https://pypi.python.org/pypi/validation>`_.

It can be installed manually using pip.

.. code:: bash

    $ pip install validation

As this library is a useful tool for cleaning up established codebases, it will
continue to support Python 2.7 for the foreseeable future.
The string validation functions are particularly handy for sorting out unicode
issues in preparation for making the jump to Python 3.

.. end-installation


Usage
-----
.. begin-usage

The validation functions provided by this library are intended to be used at
the head of public functions to check their arguments.

.. code:: python

    from validation import (
        validate_int, validate_float,
        validate_structure,
        validate_text,
    )


    def function(int_arg, dict_arg, unicode_arg=None):
        """
        A normal function that expects to be called in a particular way.

        :param int int_arg:
            A non-optional integer.  Must be between one and ten.
        :param dict dict_arg:
            A dictionary containing an integer ID, and a floating point amount.
        :param str unicode_arg:
            An optional string.
        """
        validate_int(int_arg, min_value=0, max_value=10)
        validate_structure(dict_arg, schema={
            'id': validate_int(min_value=0)
            'amount': validate_float(),
        })
        validate_text(unicode_argument, required=False)

        # Do something.
        ...


Exceptions raised by the validation functions are allowed to propagate through.
Everything is inline, with no separate schema object or function.

.. end-usage


Design
------
.. begin-design

What `validation` does
~~~~~~~~~~~~~~~~~~~~~~
This library contains a number of functions that will check their first
argument if one is provided, or return a closure that can be used later.

Functions check values against a semantic type, not a concrete type.
``validate_structure`` and ``validate_mapping`` both expect dictionaries, but
differ in whether they treat the keys as names or keys.
``validate_text`` exists, but we also provide special validators
for email addresses and domain names.

Functions are fairly strict by default.
``validate_float``, for example, will reject ``NaN`` unless explicitly allowed.
On Python 2 ``validate_text`` will enforce the use of unicode.

Intended to be mixed with normal Python code to perform more complex
validation.
As an example, the library provides no tools to assert that to values are
mutually exclusive as this requirement is much more clearly expressed with a
simple ``if`` block.

Basic support for validating simple data-structures is implemented.


What `validation` does not do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``validation`` library is not a schema definition language.
Validation functions and closures are not designed to be introspectable, and
are expected to be used inline.

It is not intended for validating serialized, or partially serialized data.
While there is some support for validating structured dictionaries, it does not
extend to handling any of the many ways to represent a sum types in json.
More complicated data-structures should generally be represented as classes,
and validation pushed to the constructors.

Exceptions raised by the validation library are not intended to be caught.
We assume that validation failures indicate that the caller is being used
incorrectly and that the error and will be interpreted by a programmer and not
the machine.

We use built-in exception classes rather than defining custom ones so that
libraries that use our functions can allow them to fall through their public
interface.

Finally, the ``validation`` library does not perform any kind of sanitization.
Its purpose is to catch mistakes, not paper over them.
Values passed in to the library will never be modified.

.. end-design


Links
-----

- Source code: https://github.com/bwhmather/python-validation
- Issue tracker: https://github.com/bwhmather/python-validation/issues
- Continuous integration: https://travis-ci.org/bwhmather/python-validation
- PyPI: https://pypi.python.org/pypi/validation


License
-------

The project is made available under the terms of the Apache 2.0 license.  See `LICENSE <./LICENSE>`_ for details.



.. end-docs
