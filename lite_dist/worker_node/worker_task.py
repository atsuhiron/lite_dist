from typing import Callable
import abc

from tqdm import tqdm

from lite_dist.common.trial import Trial
from lite_dist.common.util_func import to_bytes
from lite_dist.worker_node.exceptions import ConfigError


class BaseWorkerTask(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, trial: Trial) -> Trial:
        pass


class HashWorkerTask(BaseWorkerTask):
    def __init__(self, hash_func: Callable[[int], bytes], thread_num: int):
        self.hash_func = hash_func
        self.thread_num = thread_num

    def run(self, trial: Trial) -> Trial:
        if self.thread_num == 1:
            preimage_or_none = self._run_with_single_thread(
                trial.target, trial.trial_range.start, trial.trial_range.size
            )
        elif self.thread_num > 1:
            preimage_or_none = self._run_with_multi_thread(
                trial.target, trial.trial_range.start, trial.trial_range.size
            )
        else:
            raise ConfigError("thread_num は1以上の値を指定してください")

        if preimage_or_none is not None:
            trial.on_resolve(preimage_or_none)
        else:
            trial.on_done()
        return trial

    def _run_with_single_thread(self, target_int: int, start_int: int, size: int) -> int | None:
        target_bytes = to_bytes(target_int)
        for value in tqdm(range(start_int, start_int + size)):
            hashed_bytes = self.hash_func(value)
            if hashed_bytes == target_bytes:
                return value
        return None

    def _run_with_multi_thread(self, target_int: int, start_int: int, size: int) -> int | None:
        pass  # TODO: Implement
        target_bytes = to_bytes(target_int)
        for value in tqdm(range(start_int, start_int + size)):
            hashed_bytes = self.hash_func(value)
            if hashed_bytes == target_bytes:
                return value
        return None
