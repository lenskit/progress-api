"""
Null backend that doesn't supply any progress.
"""
from __future__ import annotations
from typing import Optional

from enlighten import Manager, Counter

from .. import api
from . import ProgressBackend, ProgressBarSpec


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
        bar = self.manager.counter(
            total=spec.total, desc=spec.label, unit=spec.unit, leave=spec.leave
        )
        bars = {spec.finish_state: bar}
        bars.update(
            (state, bar.add_subcounter()) for state in spec.states if state != spec.finish_state
        )

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
            state = self.spec.finish_state
        bar = self.bars[state]
        if src_state:
            src = self.bars[src_state]
            bar.update_from(src, n)
        else:
            bar.update(n)

    def finish(self):
        self.bar.close()
