"""
Backend-agnostic API for reporting progress.
"""

from importlib.metadata import version, PackageNotFoundError

from .api import Progress, make_progress  # noqa: F401
from .config import set_backend  # noqa: F401


try:
    __version__ = version("progress-api")
except PackageNotFoundError:
    # package is not installed
    pass
