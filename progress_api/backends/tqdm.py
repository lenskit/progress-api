# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Progress bar backend for `tqdm`_.  This backend is quite limited;
it does not support multiple states, and it does not have good
support for multiple progress bars or inteaction with logging,
unless used in a Jupyter notebook environment.

.. _tqdm: https://tqdm.github.io/docs/tqdm/
"""
# pyright: basic
from __future__ import annotations

from typing import Optional

from tqdm import tqdm
from tqdm.auto import tqdm as auto_tqdm

from .. import api
from . import ProgressBackend, ProgressBarSpec


class TQDMProgressBackend(ProgressBackend):
    """
    TQDM progress bar backend implementation.
    """

    tqdm: type[tqdm]

    def __init__(self, tqdm: type[tqdm] = auto_tqdm):
        self.tqdm = tqdm

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        tqdm = self.tqdm(total=spec.total, desc=spec.label, unit=spec.unit, leave=spec.leave)  # type: ignore
        return TQDMProgress(spec, tqdm)


class TQDMProgress(api.Progress):
    spec: ProgressBarSpec
    tqdm: tqdm
    final_states: set[str]

    def __init__(self, spec: ProgressBarSpec, tqdm: "tqdm"):
        self.spec = spec
        self.tqdm = tqdm
        self.final_states = set(s.name for s in spec.states if s.final)

    def set_label(self, label: Optional[str]):
        self.tqdm.set_description(label)

    def set_total(self, total: int):
        self.tqdm.total = total

    def update(self, n: int = 1, state: Optional[str] = None, src_state: Optional[str] = None):
        if state is None or state in self.final_states and src_state not in self.final_states:
            self.tqdm.update(n)

    def finish(self):
        self.tqdm.close()
