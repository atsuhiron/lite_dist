import time
from multiprocessing.pool import Pool

from lite_dist.config import CONFIG
from lite_dist.common.util_func import from_hex
from lite_dist.common.trial import Trial, TrialRange, TrialStatus
from lite_dist.common.enums import HashMethod
from lite_dist.worker_node.worker_task import HashWorkerTask
from lite_dist.worker_node.worker import md5


def benchmark():
    chunk_sizes = [2**p for p in range(15)]
    times = []
    target = from_hex("caf9b6b99962bf5c2264824231d7a40c")

    for cs in chunk_sizes:
        task = HashWorkerTask(md5, True, cs)
        trial = Trial("benchmark", "benchmark", TrialRange(0, 2**21), target, HashMethod.MD5, TrialStatus.RESERVED)

        with Pool(CONFIG.worker.get_thread_num()) as pool:
            start = time.time()
            task.run(trial, pool)
            elapsed = time.time() - start

        times.append(elapsed)

    for cs, et in zip(chunk_sizes, times):
        print(f"chunk_size={cs:5d}  time[s]={et:.3f}")