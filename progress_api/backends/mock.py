# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Mock backend that records progress updates for testing.
"""

from __future__ import annotations

from typing import Optional

from .. import api
from . import ProgressBackend, ProgressBarSpec


class MockProgressBackend(ProgressBackend):
    """
    Progress bar backend that records progress updates in a list for testing.
    """

    record: list[str]

    def __init__(self) -> None:
        super().__init__()
        self.record = []

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        self.record.append(f"start {spec.label} {spec.total}")
        return MockProgress(self, spec)


class MockProgress(api.Progress):
    backend: MockProgressBackend

    def __init__(self, backend: MockProgressBackend, spec: ProgressBarSpec):
        self.backend = backend
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
        self.backend.record.append(f"update {self.spec.label} {n} ({src_state} -> {state})")

    def finish(self):
        self.backend.record.append(f"finish {self.spec.label}")
