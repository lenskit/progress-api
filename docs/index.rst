Welcome to the Progress API
===========================

This package provides a backend-agnostic API for reporting progress, so that
libraries can report progress information without being tied to specific
progress bar libraries.  It also provides several backend implementations,
including `tqdm`_ and `enlighten`_.  New backends can be registered as entry
points (see :ref:`implementing-backends`).

The progress API provides a good deal of flexibility; in particular, it allows
multiple states that some backends may report with different colors or other
distinguishing visuals (see :ref:`states`).  Progress reports are also attached
to Python loggers, for backends that may wish to report through the logging
framework or use the logging configuration to determine which progress bars
to display.

.. _tqdm: https://tqdm.github.io/
.. _enlighten: https://python-enlighten.readthedocs.io/en/stable/

Documentation Sections
----------------------

.. toctree::
    :maxdepth: 2

    api
    backends/index
