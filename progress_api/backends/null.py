# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Null backend that doesn't supply any progress.
"""

from __future__ import annotations

from typing import Optional

from .. import api
from . import ProgressBackend, ProgressBarSpec


class NullProgressBackend(ProgressBackend):
    """
    Progress bar backend that doesn't emit any progress.
    """

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        return NullProgress(spec)


class NullProgress(api.Progress):
    def __init__(self, spec: ProgressBarSpec):
        self.spec = spec

    def set_label(self, label: Optional[str]):
        pass

    def set_total(self, total: int):
        pass

    def update(
        self,
        n: int = 1,
        state: Optional[str] = None,
        src_state: Optional[str] = None,
        metric: int | str | float | None = None,
    ):
        pass

    def finish(self):
        pass
