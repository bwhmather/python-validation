.. _installation:

============
Installation
============

.. include:: ../README.rst
  :start-after: begin-installation
  :end-before: end-installation


Versioning
~~~~~~~~~~

This library strictly follows the `semantic versioning scheme <http://semver.org>`_.
Due to the libraries limited scope we can be fairly explicit about what changes
can be expected in a release.

Changes that will require a major version bump:
  - Removing validation functions.
  - Removing or changing the meaning of arguments to validation functions.
  - Increasing the strictness of any existing validation function.  If a value
    passes validation by an older version with the same major version, it will
    pass validation with a newer version.
  - Introducing new external dependencies.
  - Anything else that would be expected to break existing users of the
    library.

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


