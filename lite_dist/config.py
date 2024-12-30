from __future__ import annotations

import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class TableNodeConfig:
    port: int
    minimum_chunk_size: int

    def __post_init__(self):
        assert TableNodeConfig.is_power_of_two(self.minimum_chunk_size), "minimum_chunk_size には2の累乗の値を指定してください"

    @staticmethod
    def is_power_of_two(n: int) -> bool:
        if n <= 0:
            return False
        return (n & (n - 1)) == 0

    @staticmethod
    def from_dict(d: dict) -> TableNodeConfig:
        return TableNodeConfig(
            port=d["port"],
            minimum_chunk_size=d["minimum_chunk_size"]
        )


@dataclasses.dataclass(frozen=True)
class WorkerNodeConfig:
    thread_num: int

    @staticmethod
    def from_dict(d: dict) -> WorkerNodeConfig:
        return WorkerNodeConfig(
            thread_num=d.get("thread_num", 0)
        )


@dataclasses.dataclass(frozen=True)
class Config:
    table: TableNodeConfig
    worker: WorkerNodeConfig

    @staticmethod
    def from_dict(d: dict) -> Config:
        return Config(
            table=TableNodeConfig.from_dict(d["table"]),
            worker=WorkerNodeConfig.from_dict(d["worker"])
        )


with open("config.json", "r") as f:
    json_dict = json.load(f)

CONFIG = Config.from_dict(json_dict)
