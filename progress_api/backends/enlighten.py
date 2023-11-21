"""
Null backend that doesn't supply any progress.
"""
from __future__ import annotations
from typing import Optional

from enlighten import Manager, Counter

from .. import api
from . import ProgressBackend, ProgressBarSpec


_dft_counter = (
    "{desc}{desc_pad}{count:H} {unit}{unit_pad}[{elapsed}, {rate:.2f}{unit_pad}{unit}/s]{fill}"
)
_byte_counter = "{desc}{desc_pad}{count:.2kB} {unit}{unit_pad}[{elapsed}, {rate:.2k}B/s]{fill}"
_dft_bar = "{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:H}/{total:H} [{elapsed}<{eta}, {rate:.2h}{unit_pad}{unit}/s]"
_byte_bar = "{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:.2k}B/{total:.2k}B [{elapsed}<{eta}, {rate:.2k}B/s]"


class EnlightenProgressBackend(ProgressBackend):
    """
    Progress bar backend that doesn't emit any progress.
    """

    manager: Manager
    state_colors: dict[str, str]

    def __init__(self, manager: Optional[Manager] = None, state_colors: dict[str, str] = None):
        if manager is None:
            manager = Manager()
        self.manager = manager
        self.state_colors = state_colors if state_colors else {}

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        assert len(spec.states) >= 1
        options = {}
        if len(spec.states) == 1:
            options["color"] = self.state_colors.get(spec.states[0], None)

        bar = self.manager.counter(
            total=float(spec.total) if spec.total is not None else None,
            desc=spec.label,
            unit=spec.unit,
            leave=spec.leave,
            bar_format=_byte_bar if spec.unit == "bytes" else _dft_bar,
            counter_format=_byte_counter if spec.unit == "bytes" else _dft_counter,
            **options,
        )
        if len(spec.states) > 1:
            # create subcounteres in reverse order
            # when there is more than 1 state, we use subcounters for everything
            bars = {
                state: bar.add_subcounter(self.state_colors.get(state, None))
                for state in reversed(spec.states)
            }
        else:
            bars = {spec.states[0]: bar}

        return EnlightenProgress(spec, bar, bars)


class EnlightenProgress(api.Progress):
    spec: ProgressBarSpec
    bar: Counter
    bars: dict[str, Counter]

    def __init__(self, spec: ProgressBarSpec, bar: Counter, bars: dict[str, Counter]):
        self.spec = spec
        self.bar = bar
        self.bars = bars

    def set_label(self, label: Optional[str]):
        self.tqdm.set_description(label)

    def set_total(self, total: int):
        self.tqdm.total = total

    def update(self, n: int = 1, state: Optional[str] = None, src_state: Optional[str] = None):
        if state is None:
            state = self.spec.states[0]
        bar = self.bars[state]
        if src_state:
            src = self.bars[src_state]
            bar.update_from(src, float(n))
        else:
            bar.update(float(n))

    def finish(self):
        self.bar.close()
