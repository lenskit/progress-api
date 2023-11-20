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


def set_backend(impl: str | backends.ProgressBackend):
    """
    Set up a progress backend.
    """
    global _backend

    if isinstance(impl, str):
        eps = entry_points(name=impl, group="progress_api.backend")
        if eps:
            impl = eps[0].load()
            impl = impl()
        else:
            raise ValueError(f"unknown progress backend {impl}")

    _backend = impl
