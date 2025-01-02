from __future__ import annotations

import dataclasses

from lite_dist.common.enums import HashMethod, TrialStatus
from lite_dist.common.util_func import to_hex, from_hex


@dataclasses.dataclass(frozen=True)
class TrialRange:
    start: int
    size: int

    def is_empty(self) -> bool:
        return self.size <= 0

    def end(self) -> int:
        return self.start + self.size - 1

    def can_merge(self, other: TrialRange) -> bool:
        if self.start < other.start:
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        if smaller.end() + 1 >= larger.start:
            return True
        return False

    def merge(self, other: TrialRange) -> TrialRange:
        if self.start < other.start:
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        overlap = larger.start - smaller.end() - 1
        return TrialRange(smaller.start, smaller.size + larger.size - overlap)

    def to_dict(self) -> dict:
        return {
            "start": to_hex(self.start),
            "size": self.size
        }

    @staticmethod
    def from_dict(d: dict) -> TrialRange:
        return TrialRange(from_hex(d["start"]), d["size"])


@dataclasses.dataclass
class Trial:
    study_id: str
    trial_id: str
    trial_range: TrialRange
    target: int
    method: HashMethod
    status: TrialStatus
    preimage: int | None = None

    def is_empty(self) -> bool:
        return self.trial_range.is_empty()

    def is_resolved(self) -> bool:
        return self.status == TrialStatus.RESOLVED

    def can_merge(self, other: Trial) -> bool:
        if self.study_id != other.study_id:
            return False
        if self.status != other.status:
            return False
        if self.preimage is not None:
            return False
        return self.trial_range.can_merge(other.trial_range)

    def merge(self, other: Trial) -> Trial:
        new_range = self.trial_range.merge(other.trial_range)
        return Trial(
            self.study_id,
            self.create_trial_hash(self.study_id, new_range),
            new_range,
            self.target,
            self.method,
            self.status,
            self.preimage
        )

    def on_resolve(self, preimage: int) -> None:
        self.preimage = preimage
        self.status = TrialStatus.RESOLVED

    def on_done(self) -> None:
        self.status = TrialStatus.DONE

    def to_dict(self) -> dict:
        return {
            "id": self.study_id,
            "range": self.trial_range.to_dict(),
            "target": to_hex(self.target),
            "method": self.method.value,
            "status": self.status.value,
            "preimage": to_hex(self.preimage)
        }

    @staticmethod
    def from_dict(d: dict) -> Trial:
        preimage = d.get("preimage")
        if isinstance(preimage, int):
            preimage = to_hex(preimage)
        elif preimage is not None:
            raise ValueError("preimage は未指定(None)か整数を指定してください")

        return Trial(
            d["id"],
            d["trial_id"],
            TrialRange.from_dict(d["range"]),
            from_hex(d["target"]),
            HashMethod(d["method"]),
            TrialStatus(d["status"]),
            preimage
        )

    @staticmethod
    def create_benchmark_trial() -> Trial:
        return Trial(
            "benchmark",
            "benchmark",
            TrialRange(0, 65536 * 64),
            8196348318185155500105808291003927362,
            HashMethod.MD5,
            TrialStatus.RESERVED
        )

    @staticmethod
    def create_trial_hash(study_id: str, trial_range: TrialRange) -> str:
        hash_int = hash((study_id, trial_range.start, trial_range.size))
        return hex(hash_int)[2:]
