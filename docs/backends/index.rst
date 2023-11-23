Backends
========

The Progress API includes the following backends:

- :py:mod:`~progress_api.backends.null`, reporting nothing.
- :py:mod:`~progress_api.backends.tqdm`, a simple TQDM-based backend.
- :py:mod:`~progress_api.backends.enlighten`, a backend based on `Enlighten`_.

.. _Enlighten: https://python-enlighten.readthedocs.io/en/stable/

Configuring the Backend
-----------------------

By default, the progress API uses the null backend.  Actual progress-reporting
backends can be configured with the ``PROGRESS_BACKEND`` environment variable,
or with the :py:func:`~progress_api.set_backend` function.

.. autofunction:: progress_api.set_backend

Provided Backends
-----------------

Enlighten
~~~~~~~~~

.. automodule:: progress_api.backends.enlighten
    :members: EnlightenProgressBackend

TQDM
~~~~

.. automodule:: progress_api.backends.tqdm
    :members: TQDMProgressBackend

Null
~~~~

.. automodule:: progress_api.backends.null
    :members: NullProgressBackend


Implementing Backends
---------------------

Backends are can be implemented with the following:

1.  Implement the :py:class:`progress_api.Progress` interface for the backend.
2.  Implement the :py:class:`progress.backends.ProgressBackend` interface to create
    progress bars using the backend.
3.  Register the progress backend with the `progress_api.backend` entry point::

        [project.entry-points."progress_api.backend"]
        enlighten = "progress_api.backends.enlighten:EnlightenProgressBackend"

.. autoclass:: progress_api.backends.ProgressBackend

Backend Data Structures
-----------------------

These types are used by the progress API to call the backend.

.. autoclass:: progress_api.backends.ProgressBarSpec
.. autoclass:: progress_api.backends.ProgressState
