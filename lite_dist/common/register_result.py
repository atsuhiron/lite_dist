from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class TrialRegisterResult:
    success: bool
    has_next: bool
    message: str | None = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "has_next": self.has_next,
            "message": self.message
        }

    @staticmethod
    def from_dict(d: dict) -> TrialRegisterResult:
        return TrialRegisterResult(
            d["success"],
            d["has_next"],
            d.get("message")
        )


@dataclasses.dataclass(frozen=True)
class StudyRegisterResult:
    success: bool
    study_id: str | None
    message: str | None = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "id": self.study_id,
            "message": self.message
        }

    @staticmethod
    def from_dict(d: dict) -> StudyRegisterResult:
        return StudyRegisterResult(
            d["success"],
            d["id"],
            d.get("message")
        )
