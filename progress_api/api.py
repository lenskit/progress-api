from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
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
            src_state: the state to move the progress items from, if applicable.
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
    outcomes: Optional[str | list[str]] = None,
    states: Optional[str | list[str]] = None,
    leave: bool = False,
) -> Progress:
    """
    Primary API for creating progress reporters.  This is the function client
    code will use the most often.

    The ``outcomes`` and ``states`` variables configure multiple states for
    multi-state progress bars.  See :ref:`states` for details on how states
    are handled and how these arguments configure them.

    Args:
        logger: The logger to attach this progress to.
        label: A label for the progress display.
        total: The total for the progress (if known).
        unit:
            A label for the units.  If 'bytes' is supplied, some backends will
            use binary suffixes (MiB, etc.).
        outcomes:
            The names of different outcomes for a multi-state progress bar
        states:
            The names of different sequential states for a multi-state progress bars.
        leave:
            Whether to leave the progress bar visible after it has finished.
    """
    if logger is None:
        logger = getLogger()
    elif isinstance(logger, str):
        logger = getLogger(logger)

    if outcomes:
        sl = [backends.ProgressState(s, True) for s in outcomes]
        if states:
            sl += [backends.ProgressState(s, False) for s in states]
    elif states:
        sl = [backends.ProgressState(s, i == 0) for (i, s) in enumerate(states)]
    else:
        sl = [backends.ProgressState("finished", True)]

    spec = backends.ProgressBarSpec(logger, label, total, unit, sl, leave)
    return config.get_backend().create_bar(spec)
