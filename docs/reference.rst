.. _reference:

=========
Reference
=========


Core Validation Functions
=========================

.. module:: validation.core

Functions for validating simple, immutable, built-in data-types.


Numbers
-------

.. autofunction:: validate_int
.. autofunction:: validate_float


Strings
-------

.. autofunction:: validate_text
.. autofunction:: validate_bytes


Time
----

.. autofunction:: validate_date
.. autofunction:: validate_datetime


Other
-----
.. autofunction:: validate_bool


Datastructure Validation Functions
==================================

.. module:: validation.datastructures

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
