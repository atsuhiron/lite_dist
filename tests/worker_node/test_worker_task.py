import pytest

from lite_dist.common.enums import HashMethod, TrialStatus
from lite_dist.common.trial import TrialRange, Trial
from lite_dist.common.util_func import to_bytes
from lite_dist.worker_node.worker_task import HashWorkerTask


def _id_hash(x: int) -> tuple[int, bytes]:
    return x, to_bytes(x)


@pytest.mark.parametrize(
    ["trial", "expected"],
    [
        pytest.param(
            Trial("", "", TrialRange(0, 10), 3, HashMethod.MD5, TrialStatus.RESERVED),
            Trial("", "", TrialRange(0, 10), 3, HashMethod.MD5, TrialStatus.RESOLVED, 3),
            id="Resolve"
        ),
        pytest.param(
            Trial("", "", TrialRange(0, 10), 100, HashMethod.MD5, TrialStatus.RESERVED),
            Trial("", "", TrialRange(0, 10), 100, HashMethod.MD5, TrialStatus.DONE),
            id="Done"
        )
    ]
)
def test_single_thread_run(trial: Trial, expected: Trial):
    sut = HashWorkerTask(_id_hash, 1)
    actual = sut.run(trial, None)
    assert actual == expected
