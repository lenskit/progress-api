from .backends import ProgressBackend
from .backends.null import NullProgressBackend

backend = NullProgressBackend()


def set_backend(impl: ProgressBackend):
    """
    Set up a progress backend.
    """
    global backend
    backend = impl
