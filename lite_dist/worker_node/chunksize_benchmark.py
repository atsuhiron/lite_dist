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
    targets = [
        from_hex("caf9b6b99962bf5c2264824231d7a40c"),
        from_hex("59bd0a3ff43b32849b319e645d4798d8a5d1e889"),
        from_hex("06271baf49532c879aa3c58b48671884bcc858f09197412d682750496c33e1e1")
    ]
    methods = [HashMethod.MD5, HashMethod.SHA1, HashMethod.SHA256]

    for target, method in zip(targets, methods):
        times = []
        for cs in chunk_sizes:
            trial = Trial("benchmark", "benchmark", TrialRange(0, 2**21), target, method, TrialStatus.RESERVED)
            task = HashWorkerTask(trial, md5, True, cs)

            with Pool(CONFIG.worker.get_thread_num()) as pool:
                start = time.time()
                task.run(pool)
                elapsed = time.time() - start

            times.append(elapsed)

        for cs, et in zip(chunk_sizes, times):
            print(f"chunk_size={cs:5d}  time[s]={et:.3f}")
