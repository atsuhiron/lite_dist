from __future__ import annotations

import dataclasses

from common.enums import HashMethod, TrialStatus
from common.util_func import to_hex, from_hex


@dataclasses.dataclass(frozen=True)
class TrialRange:
    start: int
    size: int

    def end(self) -> int:
        return self.start + self.size

    def can_merge(self, other: TrialRange) -> bool:
        self_end = self.end()
        other_end = other.end()
        if self_end + 1 >= other.start or other_end + 1 >= self.start:
            return True
        return False

    def merge(self, other: TrialRange) -> TrialRange:
        if self.start < other.start:
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        overlap = larger.start - smaller.end() + 1
        return TrialRange(smaller.start, smaller.size + larger.size - overlap)

    def to_dict(self) -> dict:
        return {
            "start": to_hex(self.start),
            "size": self.size
        }

    @staticmethod
    def from_dict(d: dict) -> TrialRange:
        return TrialRange(from_hex(d["start"]), d["size"])


@dataclasses.dataclass(frozen=True)
class Trial:
    trial_id: str
    trial_range: TrialRange
    target: int
    method: HashMethod
    status: TrialStatus

    def can_merge(self, other: Trial) -> bool:
        if self.trial_id != other.trial_id:
            return False
        if self.status != other.status:
            return False
        return self.trial_range.can_merge(other.trial_range)

    def merge(self, other: Trial) -> Trial:
        return Trial(
            self.trial_id,
            self.trial_range.merge(other.trial_range),
            self.target,
            self.method,
            self.status
        )

    def to_dict(self) -> dict:
        return {
            "id": self.trial_id,
            "range": self.trial_range.to_dict(),
            "target": self.target,
            "method": self.method.value,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(d: dict) -> Trial:
        return Trial(
            d["id"],
            TrialRange.from_dict(d["range"]),
            from_hex(d["target"]),
            HashMethod(d["method"]),
            TrialStatus(d["status"])
        )
