from typing import Callable
import abc
from multiprocessing.pool import Pool

from tqdm import tqdm

from lite_dist.common.trial import Trial
from lite_dist.common.util_func import to_bytes
from lite_dist.worker_node.exceptions import ConfigError


class BaseWorkerTask(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, pool: Pool | None) -> Trial:
        pass


class HashWorkerTask(BaseWorkerTask):
    def __init__(self, trial: Trial, hash_func: Callable[[int], tuple[int, bytes]], do_multithread: bool, chunk_size: int | None = None):
        self.trial = trial
        self.hash_func = hash_func
        self.do_multithread = do_multithread
        self.chunk_size = chunk_size or 1024

    def run(self, pool: Pool | None) -> Trial:
        if (not self.do_multithread) or pool is None:
            preimage_or_none = self._run_with_single_thread(
                self.trial.target, self.trial.trial_range.start, self.trial.trial_range.size
            )
        elif self.do_multithread and pool is not None:
            preimage_or_none = self._run_with_multi_thread(
                pool, self.trial.target, self.trial.trial_range.start, self.trial.trial_range.size
            )
        else:
            raise ConfigError("thread_num は1以上の値を指定してください")

        if preimage_or_none is not None:
            self.trial.on_resolve(preimage_or_none)
        else:
            self.trial.on_done()
        return self.trial

    def _run_with_single_thread(self, target_int: int, start_int: int, size: int) -> int | None:
        target_bytes = to_bytes(target_int)
        for value in tqdm(range(start_int, start_int + size)):
            _, hashed_bytes = self.hash_func(value)
            if hashed_bytes == target_bytes:
                return value
        return None

    def _run_with_multi_thread(self, pool: Pool, target_int: int, start_int: int, size: int) -> int | None:
        target_bytes = to_bytes(target_int)
        with tqdm(total=size) as pbar:
            for value, hashed_bytes in pool.imap_unordered(self.hash_func, range(start_int, start_int + size), chunksize=self.chunk_size):
                if hashed_bytes == target_bytes:
                    return value
                pbar.update()
