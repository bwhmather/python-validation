.. _installation:

============
Installation
============

.. include:: ../README.rst
  :start-after: begin-installation
  :end-before: end-installation


Versioning
~~~~~~~~~~

This library follows the `semantic versioning scheme <http://semver.org>`_.
Broadly speaking, major versions contain breaks in backwards compatibility,
minor versions contain changes that might prevent reverting to an earlier
version, and patch versions contain only minor bug fixes and documentation
improvements.

Prior to version 1.0, all releases can contain breaking changes.

As this library is likely to be used independently by multiple libraries that
are included by a single project, we have to be more careful about what changes
we allow in new major versions.
As a rule, it should always be possible to write code that is compatible with
two consecutive major versions.
Most changes that would be allowed by a strict reading of the semantic
versioning rules will be avoided or require the project to move to a new
namespace.

Due to the library's limited scope we can be quite explicit about what changes
can be expected in a release.

Kinds of change that would require the project to be released under a new
namespace:
  - Removing validation functions.
  - Removing or changing the meaning of arguments to validation functions.
  - Increasing the strictness of any existing validation function.  If a value
    passes validation by an older version with the same major version, it will
    pass validation with a newer version.
  - Introducing new external dependencies.
  - Anything else that would be expected to break existing users of the
    library.

Kinds of changes that require a major version bump:
  - Dropping support for older versions of python.

Kinds of change that require a minor version bump:
  - Adding new validation functions.
  - Adding new arguments to existing validation functions.
  - Relaxing the strictness of any existing validation function.
  - Any other changes that users of the library could use that would prevent
    their code from working with an older version.

Kinds of change that require only a patch version bump:
  - **Changes to exception messages.**
  - **Changes to the order in which conditions that result in the same
    exception are checked.**
  - Bug-fixes that do not affect the expected behaviour.
  - Documentation improvements.
  - Re-releases to fix packaging issues.

Libraries should specify a minimum minor version and maximum major version.
Applications should do the same but are encouraged to pin a particular version
for releases.

Patches to backport bug-fixes will only be accepted for the latest minor
versions of each major version.
Only the latest major version will be actively supported.
