from lite_dist.common.enums import HashMethod, TrialStatus
from lite_dist.common.trial import TrialRange, Trial
from lite_dist.table_node.study import Study


def _create_study_from_ranges(ranges: list[TrialRange], status_list: list[TrialStatus] | None = None) -> Study:
    if status_list is None:
        status_list = [TrialStatus.DONE] * len(ranges)

    return Study("", 0, HashMethod.MD5, [Trial("", "", tr, 0, HashMethod.MD5, st) for tr, st in zip(ranges, status_list)])


def test_table_simplify_empty():
    ranges = []
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 0


def test_table_simplify_single_reserved():
    ranges = [
        TrialRange(0, 100)
    ]
    study = _create_study_from_ranges(ranges, [TrialStatus.RESERVED])
    study.simplify_table()
    assert len(study.trial_table) == 1
    assert study.trial_table[0].trial_range == TrialRange(0, 100)


def test_table_simplify_single():
    ranges = [
        TrialRange(0, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 1
    assert study.trial_table[0].trial_range == TrialRange(0, 100)


def test_table_simplify_far_double():
    ranges = [
        TrialRange(0, 100),
        TrialRange(200, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 2
    assert study.trial_table[0].trial_range == TrialRange(0, 100)
    assert study.trial_table[1].trial_range == TrialRange(200, 100)


def test_table_simplify_adjacency_double():
    ranges = [
        TrialRange(0, 100),
        TrialRange(100, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 1
    assert study.trial_table[0].trial_range == TrialRange(0, 200)


def test_table_simplify_adjacency_2_doubles():
    ranges = [
        TrialRange(0, 100),
        TrialRange(100, 100),
        TrialRange(10000, 100),
        TrialRange(10100, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 2
    assert study.trial_table[0].trial_range == TrialRange(0, 200)
    assert study.trial_table[1].trial_range == TrialRange(10000, 200)


def test_table_simplify_adjacency_triple():
    ranges = [
        TrialRange(0, 100),
        TrialRange(100, 100),
        TrialRange(200, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    assert len(study.trial_table) == 1
    assert study.trial_table[0].trial_range == TrialRange(0, 300)


def test_table_simplify_mix():
    ranges = [
        TrialRange(0, 100),
        TrialRange(100, 100),
        TrialRange(200, 100),
        TrialRange(1000, 10),
        TrialRange(8090, 10),
        TrialRange(8100, 50),
        TrialRange(300, 100)
    ]
    study = _create_study_from_ranges(ranges)
    study.simplify_table()
    sorted_range = sorted(study.trial_table, key=lambda tri: tri.trial_range.start)
    assert len(sorted_range) == 3
    assert sorted_range[0].trial_range == TrialRange(0, 400)
    assert sorted_range[1].trial_range == TrialRange(1000, 10)
    assert sorted_range[2].trial_range == TrialRange(8090, 60)
