"""
Package containing backends and the backend interface for the progress API. This
package provides several backends, but the API is not limited to the supplied
backends.
"""

from abc import ABC, abstractmethod
from typing import Optional
from logging import Logger
from dataclasses import dataclass
from progress_api import Progress


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
    List of states for backends that support multiple progress bars.  If no
    states were specified by the caller, this contains one state ``'finished'``.
    """
    states: list[str] = ["finished"]
    """
    The name of the state designaged for completed or finished tasks.
    """
    finish_state: str = "finished"


class ProgressBackend(ABC):
    """
    Interface to be implemented by progress API backends.
    """

    @abstractmethod
    def create_bar(self, spec: ProgressBarSpec) -> Progress:
        """
        Create a new progress bar from the given specification.
        """
        raise NotImplementedError()
