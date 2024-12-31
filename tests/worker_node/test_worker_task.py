import pytest

from lite_dist.common.enums import HashMethod, TrialStatus
from lite_dist.common.trial import TrialRange, Trial
from lite_dist.worker_node.worker_task import HashWorkerTask


@pytest.mark.parametrize(
    ["trial", "expected"],
    [
        pytest.param(
            Trial("", TrialRange(0, 10), 3, HashMethod.MD5, TrialStatus.RESERVED),
            Trial("", TrialRange(0, 10), 3, HashMethod.MD5, TrialStatus.RESOLVED, 3),
            id="Resolve"
        ),
        pytest.param(
            Trial("", TrialRange(0, 10), 100, HashMethod.MD5, TrialStatus.RESERVED),
            Trial("", TrialRange(0, 10), 100, HashMethod.MD5, TrialStatus.DONE),
            id="Done"
        )
    ]
)
def test_single_thread_run(trial: Trial, expected: Trial):
    sut = HashWorkerTask(lambda x: x, 1)
    actual = sut.run(trial)
    assert actual == expected
