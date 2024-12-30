from __future__ import annotations

import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class Config:
    port: int
    minimum_chunk_size: int

    def __post_init__(self):
        assert Config.is_power_of_two(self.minimum_chunk_size), "minimum_chunk_size には2の累乗の値を指定してください"

    @staticmethod
    def is_power_of_two(n: int) -> bool:
        if n <= 0:
            return False
        return (n & (n - 1)) == 0

    @staticmethod
    def from_dict(d: dict) -> Config:
        return Config(
            port=d["port"],
            minimum_chunk_size=d["minimum_chunk_size"]
        )


with open("config.json", "r") as f:
    json_dict = json.load(f)

CONFIG = Config.from_dict(json_dict)
