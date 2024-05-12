# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Package containing backends and the backend interface for the progress API. This
package provides several backends, but the API is not limited to the supplied
backends.
"""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from logging import Logger
from typing import Literal, NamedTuple, Optional, TypeAlias

from .. import api

ErrorAction: TypeAlias = Literal["ignore", "warn", "fail"]


class ProgressState(NamedTuple):
    """
    Representation of a progress bar state.
    """

    name: str
    """
    The state name.
    """

    final: bool = True
    """
    Whether this is a final state (an outcome).  Backends that do not support
    multiple states should report the sum of all final states.
    """


@dataclass
class ProgressBarSpec:
    """
    Class encapsulating a progress bar specification to request a new progress
    bar from the backend.
    """

    logger: Logger
    """
    The logger this progress bar is attached to.
    """
    label: Optional[str] = None
    """
    The progress bar label (called a description in some backends).
    """
    total: Optional[int] = None
    """
    The initial total number of tasks/bytes/objects in the progress bar.
    """
    unit: Optional[str] = None
    """
    The progress bar's units.  Backens that support binary byte counts should
    recognize the ``bytes`` unit here.
    """
    states: list[ProgressState] = field(default_factory=lambda: [ProgressState("finished")])
    """
    List of progress states.  If no states were specified by the caller, this
    contains one final state ``'finished'``.
    """
    leave: bool = False
    """
    Whether the progress bar should remain visible after completion.
    """

    def check_state(self, state: str, action: ErrorAction = "warn") -> bool:
        """
        Check whether the specified state is valid.
        """
        for cs in self.states:
            if cs.name == state:
                return True

        if action == "fail":
            raise ValueError(f"undefined progress state {state}")
        elif action == "warn":
            warnings.warn(f"undefined progress state {state}")

        return False


class ProgressBackend(ABC):
    """
    Interface to be implemented by progress API backends.

    .. note::
        Progress backends must be thread-safe.
    """

    @abstractmethod
    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        """
        Create a new progress bar from the given specification.
        """
        raise NotImplementedError()
