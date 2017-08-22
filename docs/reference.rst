.. _reference:

=========
Reference
=========


Core Validation Functions
=========================


Functions for validating simple, immutable, built-in data-types.


Numbers
-------

.. module:: validation.number

.. autofunction:: validate_int
.. autofunction:: validate_float


Strings
-------

.. module:: validation.string

.. autofunction:: validate_text
.. autofunction:: validate_bytes


Time
----

.. module:: validation.datetime

.. autofunction:: validate_date
.. autofunction:: validate_datetime


Other
-----

.. module:: validation.core

.. autofunction:: validate_bool


Datastructure Validation Functions
==================================

.. module:: validation.datastructure

Functions for validating plain data-structures.


Sequences
---------

.. autofunction:: validate_list
.. autofunction:: validate_set
.. autofunction:: validate_tuple


Dictionaries
------------

.. autofunction:: validate_mapping
.. autofunction:: validate_structure


Enumerations
------------

.. autofunction:: validate_enum
