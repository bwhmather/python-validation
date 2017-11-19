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

A simple python library containing functions that check python values.
It is intended to make it easy to verify commonly expected pre-conditions on
arguments to functions.


What `validation` does:
~~~~~~~~~~~~~~~~~~~~~~~
Functions validate their first argument or return a closure.

Functions check values against a semantic type, not a concrete type.
``validate_structure`` and ``validate_mapping`` both expect dictionaries, but
differ in whether they treat the keys as names or keys.
``validate_text`` exists, but we also provide special validators
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


Installation
------------
.. begin-installation

The ``validation`` library is available on `pypi <https://pypi.python.org/pypi/validation>`_.

It can be installed manually using pip.

.. code:: bash

    $ pip install validation

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
