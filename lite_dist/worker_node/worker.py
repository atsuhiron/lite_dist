import hashlib
import time
import math
import logging
from multiprocessing.pool import Pool

from lite_dist.config import CONFIG
from lite_dist.common.trial import Trial
from lite_dist.common.enums import HashMethod
from lite_dist.common.util_func import to_bytes
from lite_dist.worker_node.table_node_client import BaseTableNodeClient
from lite_dist.worker_node.worker_task import BaseWorkerTask, HashWorkerTask


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def md5(x: int) -> tuple[int, bytes]:
    return x, hashlib.md5(to_bytes(x)).digest()


def sha1(x: int) -> tuple[int, bytes]:
    return x, hashlib.sha1(to_bytes(x)).digest()


def sha256(x: int) -> tuple[int, bytes]:
    return x, hashlib.sha256(to_bytes(x)).digest()


class Worker:
    def __init__(self, table_node_client: BaseTableNodeClient):
        self.client = table_node_client
        if CONFIG.worker.get_thread_num() == 1:
            self.pool = None
        else:
            self.pool = Pool(CONFIG.worker.get_thread_num())

    def start(self):
        ping_ok = self.client.ping_table_server()
        if not ping_ok:
            logger.info("Failed to connect to table node server.")
            return

        if CONFIG.worker.trial_size_ratio <= 0:
            logger.info("Benchmark capacity of this machine")
            tsr = self._measure_trial_ratio_size()
        else:
            tsr = CONFIG.worker.trial_size_ratio
        logger.info("Trial size ratio is: %d" % tsr)

        while True:
            self._step(tsr * CONFIG.common.minimum_chunk_size)

    def _step(self, max_size: int) -> None:
        trial = self.client.reserve_trial(max_size)
        if trial.is_empty():
            logger.info("No study. sleep %d sec" % CONFIG.worker.sleep_sec_on_empty)
            time.sleep(CONFIG.worker.sleep_sec_on_empty)
            return

        task = self.map_worker_task(trial)
        trial = task.run(self.pool)
        _ = self.client.register_trial(trial)

    @staticmethod
    def _measure_trial_ratio_size() -> int:
        benchmark_trial = Trial.create_benchmark_trial()
        wt = HashWorkerTask(benchmark_trial, md5, False)

        start_time = time.time()
        wt.run(None)
        elapsed = time.time() - start_time
        logger.info(elapsed)

        # 1 秒で 64 倍になるようにする
        log_cap = math.log2(elapsed)
        ratio_power = int(log_cap + 0.5) + 6
        return 2 ** ratio_power

    @staticmethod
    def map_worker_task(trial: Trial) -> BaseWorkerTask:
        match trial.method:
            case HashMethod.MD5:
                return HashWorkerTask(trial, md5, CONFIG.worker.get_thread_num() > 1)
            case HashMethod.SHA1:
                return HashWorkerTask(trial, sha1, CONFIG.worker.get_thread_num() > 1)
            case HashMethod.SHA256:
                return HashWorkerTask(trial, sha256, CONFIG.worker.get_thread_num() > 1)
            case _:
                raise ValueError("不明なメソッドです: %s" % trial.method.name)
