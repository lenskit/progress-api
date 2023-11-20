from abc import ABC, abstractmethod
from typing import Optional
from logging import Logger


class Progress(ABC):
    """
    Uniform interface to progress reporting APIs.

    Attributes:
        name: The name of the logger this progress bar is attached to.
    """

    name: str

    @abstractmethod
    def set_label(self, label: Optional[str]):
        """
        Set a label to be used for this progress bar.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_total(self, total: int):
        """
        Update the progress bar's total.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, n: int = 1, state: Optional[str] = None, src_state: Optional[str] = None):
        """
        Update the progress bar.

        Args:
            n: the amount to increment the progress bar counter by.
            state: the name of the progress bar state to increment.
            src_state: the state to move the progress items from, if applicable.
        """
        raise NotImplementedError()

    @abstractmethod
    def finish(self):
        """
        Finish and close this progress bar, releasing resources as appropriate.
        """
        raise NotImplementedError()


def progress(
    logger: Optional[str | Logger] = None,
    label: Optional[str] = None,
    total: Optional[int] = None,
    unit: Optional[str] = None,
    states: Optional[list[str]] = None,
    finish_state: Optional[str] = None,
):
    """
    Create a progress bar.

    Args:
        logger: The logger to attach this progress to.
        label: A label for the progress display.
        total: The total for the progress (if known).
        unit:
            A label for the units.  If 'bytes' is supplied, some backends will
            use binary suffixes (MiB, etc.).
        states:
            A label for different states to display, when displaying a multi-state
            progress bar.  Not all backends support multiple states.  States are
            typically displayed in order.  Callers do not need to supply an
            unfinished state.
        finish_state:
            The label for the “finished” state.  If this is not supplied, a state
            named “finished” is used if supplied in “states”; otherwise, the first
            state in “states” is considered finished.
    """
    pass
