"""
Null backend that doesn't supply any progress.
"""

from typing import Optional
from . import ProgressBackend, Progress, ProgressBarSpec


class NullProgressBackend(ProgressBackend):
    """
    Progress bar backend that doesn't emit any progress.
    """

    def create_bar(self, spec: ProgressBarSpec) -> Progress:
        return NullProgress()


class NullProgress(Progress):
    def set_label(self, label: Optional[str]):
        pass

    def set_total(self, total: int):
        pass

    def update(self, n: int = 1, state: Optional[str] = None, src_state: Optional[str] = None):
        pass

    def finish(self):
        pass
