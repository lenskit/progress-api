from __future__ import annotations
import threading
import os
from importlib.metadata import entry_points

from . import backends

_backend_lock = threading.Lock()
_backend = None


def _lazy_init():
    if _backend is not None:
        return

    env = os.environ.get("PROGRESS_BACKEND", None)
    if env:
        set_backend(env)
    else:
        from .backends.null import NullProgressBackend

        set_backend(NullProgressBackend())


def get_backend() -> backends.ProgressBackend:
    global _backend
    if threading.active_count() <= 1:
        _lazy_init()
    else:
        with _backend_lock:
            _lazy_init()

    return _backend


def set_backend(
    impl: str | backends.ProgressBackend | type[backends.ProgressBackend], *args, **kwargs
):
    """
    Set the progress backend.  The backend can be specified in one of several ways:

    *   A string naming a progress backend.  For the backends included with Progress API,
        this name matches the implementing module name (e.g. ``"enlighten"``).  Other
        backends can be registered with an entry point (see :ref:`implementing-backends`).
    *   An object implementing the :class:`backends.ProgressBackend` interface.
    *   A subclass of :class:`backends.ProgressBackend` that to instantiate.

    If the backend is a class (ether a class object, or a backend name), then it is
    instantiated witht he supplied ``args`` and ``kwargs``.

    Args:
        impl: The implementation.
        *args, **kwargs: Arguments to pass to the implementation constructor.
    """
    global _backend

    if isinstance(impl, str):
        eps = entry_points(name=impl, group="progress_api.backend")
        if eps:
            impl = eps[0].load()
        else:
            raise ValueError(f"unknown progress backend {impl}")

    if isinstance(impl, type):
        impl = impl(*args, **kwargs)
    _backend = impl
