from __future__ import annotations

import dataclasses
import json
import os

from lite_dist.common.util_func import is_power_of_two


@dataclasses.dataclass(frozen=True)
class CommonConfig:
    minimum_chunk_size: int

    def __post_init__(self):
        assert is_power_of_two(self.minimum_chunk_size), "minimum_chunk_size には2の累乗の値を指定してください"

    @staticmethod
    def from_dict(d: dict) -> CommonConfig:
        return CommonConfig(
            minimum_chunk_size=d["minimum_chunk_size"]
        )


@dataclasses.dataclass(frozen=True)
class TableNodeConfig:
    port: int

    @staticmethod
    def from_dict(d: dict) -> TableNodeConfig:
        return TableNodeConfig(
            port=d["port"]
        )


@dataclasses.dataclass(frozen=True)
class WorkerNodeConfig:
    thread_num: int
    trial_size_ratio: int
    sleep_sec_on_empty: int

    def __post_init__(self):
        assert is_power_of_two(self.trial_size_ratio) or self.trial_size_ratio == 0, "trial_size_ratio には2の累乗か0を指定してください"
        assert self.sleep_sec_on_empty >= 0, "sleep_sec_on_empty は正の値にしてください"

    def get_thread_num(self) -> int:
        if self.thread_num <= 0:
            return os.cpu_count()
        return self.thread_num

    @staticmethod
    def from_dict(d: dict) -> WorkerNodeConfig:
        return WorkerNodeConfig(
            thread_num=d.get("thread_num", 0),
            trial_size_ratio=d.get("trial_size_ratio", 0),
            sleep_sec_on_empty=d.get("sleep_sec_on_empty", 10)
        )


@dataclasses.dataclass(frozen=True)
class Config:
    common: CommonConfig
    table: TableNodeConfig
    worker: WorkerNodeConfig

    @staticmethod
    def from_dict(d: dict) -> Config:
        return Config(
            common=CommonConfig.from_dict(d["common"]),
            table=TableNodeConfig.from_dict(d["table"]),
            worker=WorkerNodeConfig.from_dict(d["worker"])
        )


with open("config.json", "r") as f:
    json_dict = json.load(f)

CONFIG = Config.from_dict(json_dict)
