from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class RegisterTrialResult:
    success: bool
    has_next: bool

    @staticmethod
    def from_dict(d: dict) -> RegisterTrialResult:
        return RegisterTrialResult(
            d["success"],
            d["has_next"]
        )
