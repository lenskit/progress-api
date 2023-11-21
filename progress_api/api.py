from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from logging import Logger, getLogger

from . import backends, config


class Progress(ABC):
    """
    Uniform interface to progress reporting APIs.

    Progress bars can be used as context managers; :meth:`finish` is called
    when the context is exited.

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
            src_state: the state to move the progress items from, if applicable.  This should
                never be supplied when ``state`` is the last state provided to {meth}`makeProgress`,
                as it is the *first* state items are considered able to enter; not all backends
                support moving into the initial state from another state.
        """
        raise NotImplementedError()

    @abstractmethod
    def finish(self):
        """
        Finish and close this progress bar, releasing resources as appropriate.
        """
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.finish()


def make_progress(
    logger: Optional[str | Logger] = None,
    label: Optional[str] = None,
    total: Optional[int] = None,
    unit: Optional[str] = None,
    states: Optional[str | List[str]] = None,
    leave: bool = False,
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
            The names of different states for a multi-state progress bar.  Not
            all backends support multiple states.  States are typically
            displayed in order; when states indicate a progression of item
            states, items are assumed to progress from the last state to the
            first. The first state is considered the “finished” state, when such
            things matter.  If not supplied, the default is a single state
            “finished”. A single state can be provided as a string for
            convenience.
        leave:
            Whether to leave the progress bar visible after it has finished.
    """
    if logger is None:
        logger = getLogger()
    elif isinstance(logger, str):
        logger = getLogger(logger)

    if not states:
        states = ["finished"]

    spec = backends.ProgressBarSpec(logger, label, total, unit, states, leave)
    return config.get_backend().create_bar(spec)
