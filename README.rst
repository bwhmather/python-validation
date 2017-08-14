Python Validation
=================

|build-status| |coverage|

.. |build-status| image:: https://travis-ci.org/JOIVY/validation/g.png?branch=develop
    :target: https://travis-ci.org/JOIVY/validation/g
    :alt: Build Status
.. |coverage| image:: https://coveralls.io/repos/JOIVY/validation/g/badge.png?branch=develop
    :target: https://coveralls.io/r/JOIVY/validation/g?branch=develop
    :alt: Coverage

.. begin-docs

A python library for runtime type checking and validation of python values.

Intended as a stepping stone towards static typing.


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
        # Validate arguments.
        validate_int(int_arg, min_value=0, max_value=10)
        validate_structure(dict_arg, schema={
            'id': validate_int(min_value=0)
            'amount': validate_float(),
        })
        validate_text(unicode_argument, required=False)

        # Do something.
        ...

The validation functions are used to check arguments passed to a public
function.
Exceptions raised by the validation functions are allowed to propagate through.
No logic is run until validation is complete.

.. end-usage

Links
-----

- Source code: https://github.com/JOIVY/validation
- Issue tracker: https://github.com/JOIVY/validation/issues
- Continuous integration: https://travis-ci.org/JOIVY/validation
- PyPI: https://pypi.python.org/pypi/validation


License
-------

The project is made available under the terms of the Apache 2.0 license.  See `LICENSE <./LICENSE>`_ for details.



.. end-docs
