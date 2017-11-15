Python Validation
=================

|build-status| |coverage|

.. |build-status| image:: https://travis-ci.org/bwhmather/python-validation.png?branch=develop
    :target: https://travis-ci.org/bwhmather/python-validation
    :alt: Build Status
.. |coverage| image:: https://coveralls.io/repos/bwhmather/python-validation/badge.png?branch=develop
    :target: https://coveralls.io/r/bwhmather/python-validation?branch=develop
    :alt: Coverage

.. begin-docs

A simple python library, intended to reduce the amount of boilerplate required
to check pre-conditions on arguments to functions.

What `validation` does:
~~~~~~~~~~~~~~~~~~~~~~~

Functions validate their first argument or return a closure.

Functions check values against a semantic type, not a concrete type.
``validate_structure`` and ``validate_mapping`` are provided to validate
dictionaries.  ``validate_text`` exists, but we also provide special validators
for email addresses and domain names.

Functions are fairly strict by default.
Designed to be mixed with normal python code to perform more complex validation



What `validation` does not:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is not a schema definition language.
Not introspectable.  Designed to be used imperatively and inline.

It is not intended for validating serialized data/json.
It does, however, provide some help validating structured and unstructured
dictionaries, as well as other data-structures.

It does not perform sanitization.
The point of this library is to catch mistakes, not paper over them


Compatibility
~~~~~~~~~~~~~
As this library is a useful tool for cleaning up established codebases, it will
continue to support python 2.7 for the foreseeable future.
The string validation functions are particularly handy for sorting out unicode
issues in preparation for making the jump to python 3.



Developed at `Joivy Ltd <https://joivy.com>`_ and open-sourced with permission.





A simple python library that provides helper functions to perform runtime type
checking and validation at api boundaries.
``validation`` is a python library for runtime type checking and validation of
python values.

It is intended to reduce the amount of boilerplate required to check simple
pre-conditions on arguments to functions.
It does not attempt to provide a full featured schema definition language for
validating untrusted data.
It also does not attempt to perform any coercion or sanitization of values.

The library provides a number of simple functions that take a value to check as
their first argument, and apply a number of

If called without a value argument, validator functions will return a closure
that can be used by other validators to check more complex data-structures.


Provides:
  - Semantically useful checks.
  - Acceptable, developer focused error messages
  - A conventions for defining new validation functions for non-standard data-
    types.

Does not provide:
  - A full schema definition language.  Typical usage will restrict what is accepted, not declare what is required.
  - Documentation generation.
  - An embedded language for checking complex data-structures.

Where it makes sense users are expected to drop back to using raw python.


By default, validation is fairly strict
Focused on checking inputs to python libraries

Does not provide a language for defining schemas

Intended as a stepping stone towards static typing.


As this library is a useful tool for cleaning up established codebases, it will
continue to support python 2.7 for the foreseeable future.
The string validation functions are particularly handy for sorting out unicode
issues in preparation for making the jump to python 3.

Developed at `Joivy Ltd <https://joivy.com>`_ and open-sourced with permission.


Installation
------------
.. begin-installation

Recommended method is to use the version from `pypi <https://pypi.python.org/pypi/validation>`_

.. code:: bash

    $ pip install validation


Please note that this library only supports python version 2.7, and versions 3.4 and later.

.. end-installation


Usage
-----
.. begin-usage

A toy example demonstrating typical usage:

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
            A dictionary containing an integer id, and a floating point amount.
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

    def function(int_arg, dict_arg, unicode_arg=None):
        if not isinstance(int_arg, int):
            raise TypeError()
        if int_arg < 0:
            raise ValueError()
        if int_arg > 10:
            raise ValueError()

        if set(dict_arg.keys()) != {'id', 'amount'}:
            raise ValueError()
        if not isinstance(dict_arg['id'], int):
            raise TypeError()
        if dict_arg.id < 0:
            raise ValueError()
        if not isinstance(dict_arg['amount'], float):
            raise TypeError()

        # And so on.
        ...



The validation functions are used to check arguments passed to a public
function.
Exceptions raised by the validation functions are allowed to propagate through.
No logic is run until validation is complete.

.. end-usage

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
