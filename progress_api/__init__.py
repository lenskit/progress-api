# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Backend-agnostic API for reporting progress.
"""

from importlib.metadata import PackageNotFoundError, version

from .api import Progress, make_progress
from .config import set_backend

__all__ = ["Progress", "make_progress", "set_backend"]

try:
    __version__ = version("progress-api")
except PackageNotFoundError:
    # package is not installed
    pass
