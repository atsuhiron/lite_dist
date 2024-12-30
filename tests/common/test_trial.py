import pytest

from lite_dist.common.trial import TrialRange


@pytest.mark.parametrize(
    ["start1", "size1", "start2", "size2", "expected"],
    [
        pytest.param(
            0, 5, 5, 3, True,
            id="true_adjacency"
        ),
        pytest.param(
            0, 10, 3, 2, True,
            id="true_contain"
        ),
        pytest.param(
            0, 10, 5, 10, True,
            id="true_overlap"
        ),
        pytest.param(
            0, 10, 11, 3, False,
            id="false_far"
        ),
        pytest.param(
            5, 3, 0, 5, True,
            id="true_adjacency_inverse"
        ),
        pytest.param(
            3, 2, 0, 10, True,
            id="true_contain_inverse"
        ),
        pytest.param(
            5, 10, 0, 10, True,
            id="true_overlap_inverse"
        ),
        pytest.param(
            11, 3, 0, 10, False,
            id="false_far_inverse"
        )
    ]
)
def test_can_merge(start1: int, size1: int, start2: int, size2: int, expected: bool):
    r1 = TrialRange(start1, size1)
    r2 = TrialRange(start2, size2)

    actual = r1.can_merge(r2)
    assert actual == expected


@pytest.mark.parametrize(
    ["range1", "range2", "expected"],
    [
        pytest.param(
            TrialRange(0, 5), TrialRange(5, 3), TrialRange(0, 8),
            id="adjacency"
        )
    ]
)
def test_merge(range1: TrialRange, range2: TrialRange, expected: TrialRange):
    actual = range1.merge(range2)
    assert actual == expected
