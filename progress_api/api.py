# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import Traceback
from logging import Logger, getLogger
from typing import Optional

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
    spec: backends.ProgressBarSpec

    @abstractmethod
    def set_label(self, label: Optional[str]) -> None:
        """
        Set a label to be used for this progress bar.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_total(self, total: int) -> None:
        """
        Update the progress bar's total.
        """
        raise NotImplementedError()

    def set_metric(
        self, label: str, value: int | str | float | None, fmt: str | None = None
    ) -> None:
        """
        Set an ”metric” on the progress bar.  This is a secondary value
        that will be displayed along with ETA; it is intended for things like a
        current measurement (e.g. the current training loss for training a
        machine learning model).

        The format specifier is put into a format string that is passed to
        :meth:`str.format`, and must include the braces.  For example, to format
        a percentage with 2 decimal points::

            progress.set_meter('buffer', buf_fill_pct, '{:.2f}%')

        Only one meter can be set at a time.  A new meter will replace any
        existing meter.  This method remembers the label and format, even
        if ``value`` is ``None``, so the metric value can be supplied in
        ``update``.

        Args:
            label: the label for the metric
            value: the metric value, or ``None`` to hide the metric.
            fmt: a format specifier (suitable for use in :meth:`str.format`)
        """
        pass

    @abstractmethod
    def update(
        self,
        n: int = 1,
        state: Optional[str] = None,
        src_state: Optional[str] = None,
        metric: int | str | float | None = None,
    ) -> None:
        """
        Update the progress bar.

        Args:
            n: the amount to increment the progress bar counter by.
            state: the name of the progress bar state to increment.
            src_state: the state to move the progress items from, if applicable.
        """
        raise NotImplementedError()

    @abstractmethod
    def finish(self) -> None:
        """
        Finish and close this progress bar, releasing resources as appropriate.
        """
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: Traceback):
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
