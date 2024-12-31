from typing import Callable
import abc

from lite_dist.worker_node.exceptions import ConfigError
from lite_dist.config import CONFIG
from lite_dist.common.trial import Trial


class BaseWorkerTask(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, trial: Trial) -> Trial:
        pass


class HashWorkerTask(BaseWorkerTask):
    def __init__(self, hash_func: Callable[[bytes], str]):
        self.hash_func = hash_func

    def run(self, trial: Trial) -> Trial:
        if CONFIG.worker.thread_num == 1:
            preimage_or_none = self._run_with_single_thread(
                trial.target, trial.trial_range.start, trial.trial_range.size
            )
        elif CONFIG.worker.thread_num > 1:
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
        target_bin = target_int.to_bytes()
        for value in range(start_int, start_int + size):
            hashed_bin = self.hash_func(value.to_bytes())
            if hashed_bin == target_bin:
                return value
        return None

    def _run_with_multi_thread(self, target_int: int, start_int: int, size: int) -> int | None:
        pass  # TODO: Implement
