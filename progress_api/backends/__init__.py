"""
Package containing backends and the backend interface for the progress API. This
package provides several backends, but the API is not limited to the supplied
backends.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List, NamedTuple
from logging import Logger
from dataclasses import dataclass, field

from .. import api


class ProgressState(NamedTuple):
    """
    Representation of a progress bar state.
    """

    """
    The state name.
    """
    name: str
    """
    Whether this is a final state (an outcome).  Backends that do not support
    multiple states should report the sum of all final states.
    """
    final: bool = True


@dataclass
class ProgressBarSpec:
    """
    Class encapsulating a progress bar specification to request a new progress
    bar from the backend.
    """

    """
    The logger this progress bar is attached to.
    """
    logger: Logger
    """
    The progress bar label (called a description in some backends).
    """
    label: Optional[str] = None
    """
    The initial total number of tasks/bytes/objects in the progress bar.
    """
    total: Optional[int] = None
    """
    The progress bar's units.  Backens that support binary byte counts should
    recognize the ``bytes`` unit here.
    """
    unit: Optional[str] = None
    """
    List of progress states.  If no states were specified by the caller, this
    contains one final state ``'finished'``.
    """
    states: List[str] = field(default_factory=lambda: [ProgressState("finished")])
    """
    Whether the progress bar should remain visible after completion.
    """
    leave: bool = False


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
