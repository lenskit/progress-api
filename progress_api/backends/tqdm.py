"""
Null backend that doesn't supply any progress.
"""
from __future__ import annotations
from typing import Optional
from .. import api
from . import ProgressBackend, ProgressBarSpec
from tqdm import tqdm
from tqdm.auto import tqdm as auto_tqdm


class TQDMProgressBackend(ProgressBackend):
    """
    Progress bar backend that doesn't emit any progress.
    """

    def __init__(self, tqdm=auto_tqdm):
        self.tqdm = tqdm

    def create_bar(self, spec: ProgressBarSpec) -> api.Progress:
        tqdm = self.tqdm(total=spec.total, desc=spec.label, unit=spec.unit)
        return TQDMProgress(spec, tqdm)


class TQDMProgress(api.Progress):
    spec: ProgressBarSpec
    tqdm: tqdm

    def __init__(self, spec: ProgressBarSpec, tqdm: tqdm):
        self.spec = spec
        self.tqdm = tqdm

    def set_label(self, label: Optional[str]):
        self.tqdm.set_description(label)

    def set_total(self, total: int):
        self.tqdm.total = total

    def update(self, n: int = 1, state: Optional[str] = None, src_state: Optional[str] = None):
        if state is None or state == self.spec.finish_state:
            self.tqdm.update(n)

    def finish(self):
        self.tqdm.close()
