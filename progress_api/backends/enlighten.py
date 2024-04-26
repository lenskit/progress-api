# This file is part of Progress API.
# Copyright (C) 2023 - 2024 Drexel University and contributors
# Licensed under the MIT license, see LICENSE.md for details.
# SPDX-License-Identifier: MIT

"""
Progress backend using `Enlighten`_ to display progress bars.  It supports
multiple bars (well) and multi-state bars, and interacts well with logging
and other output to standard output and error streams.
"""

# pyright: basic
from __future__ import annotations

from typing import Optional

from enlighten import Counter, Manager

from progress_api.util import format_metric

from .. import api
from . import ProgressBackend, ProgressBarSpec

_lead = "{desc}{desc_pad}"
_dft_meter = "[{elapsed}, {rate:.2f}{unit_pad}{unit}/s{meter_pad}{meter}]"
_byte_meter = "[{elapsed}, {rate:.2j}B/s{meter_pad}{meter}]"
_bar = "{percentage:3.0f}%|{bar}|"

_dft_counter = "".join([_lead, "{count:H} {unit}{unit_pad}", _dft_meter, "{fill}"])
_byte_counter = "".join([_lead, "{count:.2kB} {unit}{unit_pad}", _byte_meter, "{fill}"])
_dft_bar = "".join(
    [
        _lead,
        _bar,
        " {count:H}/{total:H} ",
        _dft_meter,
    ]
)
_byte_bar = "".join(
    [
        _lead,
        _bar,
        " {count:.2k}B/{total:.2k}B ",
        _byte_meter,
    ]
)


class EnlightenProgressBackend(ProgressBackend):
    """
    Progress bar backend that doesn't emit any progress.
    """

    manager: Manager
    state_colors: dict[str, str]

    def __init__(
        self, manager: Optional[Manager] = None, state_colors: dict[str, str] | None = None
    ):
        if manager is None:
            manager = Manager()
        self.manager = manager
        self.state_colors = state_colors if state_colors else {}

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        assert len(spec.states) >= 1
        options = {}
        if len(spec.states) == 1:
            color, _f = spec.states[0]
            options["color"] = self.state_colors.get(color, None)  # type: ignore

        bar = self.manager.counter(
            total=float(spec.total) if spec.total is not None else None,
            desc=spec.label,
            unit=spec.unit,
            leave=spec.leave,
            fields={"meter_pad": "", "meter": ""},
            bar_format=_byte_bar if spec.unit == "bytes" else _dft_bar,
            counter_format=_byte_counter if spec.unit == "bytes" else _dft_counter,
            **options,
        )
        if len(spec.states) > 1:
            # create subcounteres in reverse order
            # when there is more than 1 state, we use subcounters for everything
            bars = {
                state: bar.add_subcounter(self.state_colors.get(state, None))
                for (state, _f) in reversed(spec.states)
            }
        else:
            bars = {spec.states[0].name: bar}

        return EnlightenProgress(spec, bar, bars)


class EnlightenProgress(api.Progress):
    spec: ProgressBarSpec
    bar: Counter
    bars: dict[str, Counter]
    _metric_display: Optional[tuple[str, Optional[str]]] = None

    def __init__(self, spec: ProgressBarSpec, bar: Counter, bars: dict[str, Counter]):
        self.spec = spec
        self.bar = bar
        self.bars = bars

    def set_label(self, label: Optional[str]):
        self.bar.desc = label

    def set_total(self, total: int):
        self.bar.total = total

    def set_metric(self, label: str, value: int | str | float | None, fmt: str | None = None):
        self._metric_display = (label, fmt)
        self._update_metric(value)

    def _update_metric(self, value: int | str | float | None):
        if self._metric_display is None:
            return

        lbl, fmt = self._metric_display
        if value:
            self.bar.fields["meter_pad"] = ", "
            self.bar.fields["meter"] = format_metric(lbl, value, fmt)
        else:
            self.bar.fields["meter_pad"] = ""
            self.bar.fields["meter"] = ""

    def update(
        self,
        n: int = 1,
        state: Optional[str] = None,
        src_state: Optional[str] = None,
        metric: int | str | float | None = None,
    ):
        if state is None:
            state = self.spec.states[0].name
        bar = self.bars[state]
        if metric is not None:
            self._update_metric(metric)
        if src_state:
            src = self.bars[src_state]
            bar.update_from(src, float(n))  # type: ignore
        else:
            bar.update(float(n))  # type: ignore

    def finish(self):
        self.bar.close()
