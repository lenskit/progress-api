"""
Backend-agnostic API for reporting progress.
"""

from .api import Progress, make_progress  # noqa: F401
from .config import set_backend  # noqa: F401

__version__ = "0.1.0"
