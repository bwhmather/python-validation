========
Tutorial
========

.. include:: ../README.rst
  :start-after: begin-usage
  :end-before: end-usage

Basics
~~~~~~

All validators are functions which take a single value to check as their
first argument, check its type and that it meets some preconditions, and raise
an exception if they find something wrong.

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

If the first argument is missing, validator functions will return a closure
that can be called later to check a value.

.. code:: python

    >>> validator = validation.validate_int(min_value=0)
    >>> validator(-1)
    Traceback (most recent call last):
        ...
    ValueError: expected value greater than 0, but got -1

This is important when using the datastructure validators.


Composing Validators
~~~~~~~~~~~~~~~~~~~~

Datastructure validation functions usually accept as an argument a function to
be applied to each of the values they contain.

.. code:: python

    >>> value = [1, -2]
    >>> validate_list(value, validator=lambda v: validate_int(v, min_value=0))
    Traceback (most recent call last):
        ...
    ValueError: invalid item at position 1: expected value greater than 0 but got -1

Having validation functions return a validator closure means that this can be
expressed more succinctly as:

.. code:: python

    >>> value = [1, -2]
    >>> validate_list(value, validator=validate_int(min_value=0))
    Traceback (most recent call last):
        ...
    ValueError: invalid item at position 1: expected value greater than 0 but got -1


Mixing with python validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

We recommend that the validation functions only be called with static
constraints.
Even where it is possible to use dynamic constraints to check a value


This example could be implemented by passing ``lower`` as ``min_value`` to
``validate_int`` when checking ``upper``, but there is a risk that the

.. code:: python

    def clamp(value, *, lower, upper):
        validate_int(lower)
        validate_int(upper)

        if lower > upper:
            raise ValueError((
                'lower bound {lower!r} is greater than upper bound {upper!r}'
            ).format(lower=lower, upper=upper))

        return min(max(lower, value), upper)


Validating iterators
~~~~~~~~~~~~~~~~~~~~

The validation functions cannot handle iterators directly as attempting to do
so would consume the iterator.

For the same reason we have not included a generic function for validating any
iterable.


You have two options:
``list`` then ``validate_list``, or validate in loop.

.. code:: python

    def process_iterable_eager(iterable):
        iterable = list(iterable)
        validate_list(iterable, validator=validate_int())

        for item in iterable:
            # Do something.
            ...

.. code:: python

    def process_iterable_lazy(iterable):
        for item in iterable:
            validate_int(item)

            # Do something
            ...

Creating new validators
~~~~~~~~~~~~~~~~~~~~~~~

TODO


Packaging new validators into a library.


Tips
~~~~

Avoid writing wrappers that hide details your code depends on.

Catch validation errors at the top level.

Alternate validation and assignment to make it clear when validation is
missing.

