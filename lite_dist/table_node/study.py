from __future__ import annotations
from functools import reduce
import uuid
import threading

from lite_dist.config import CONFIG
from lite_dist.common.trial import Trial
from lite_dist.common.enums import HashMethod, TrialStatus, TrialSuggestMethod
from lite_dist.common.util_func import from_hex, to_hex
from lite_dist.table_node.trial_suggest_strategy import BaseTrialSuggestStrategy, SequentialTrialSuggestStrategy


_TRIAL_SUGGEST: dict[TrialSuggestMethod: BaseTrialSuggestStrategy] = {
    TrialSuggestMethod.SEQUENTIAL: SequentialTrialSuggestStrategy()
}


class Study:
    def __init__(self, study_id: str, target: int, method: HashMethod, trial_table: list[Trial]):
        self.study_id = study_id
        self.target = target
        self.method = method
        self.trial_table = trial_table
        self.result = None

        self._table_lock = threading.Lock()
        self.current_max = 0

    def simplify_table(self) -> None:
        new_table: list[Trial] = []
        mergeables: dict[int, set[int]] = {}
        trial_num = len(self.trial_table)

        with self._table_lock:
            for i in range(trial_num):
                if self.trial_table[i].status != TrialStatus.DONE:
                    continue

                for j in range(i + 1, trial_num):
                    if self.trial_table[i].can_merge(self.trial_table[j]):
                        if i in mergeables.keys():
                            mergeables[i].add(j)
                        else:
                            mergeables[i] = {j}

            mergeable_group: list[set[int]] = []
            for i in mergeables.keys():
                grouplet = mergeables[i].union({i})
                for g in range(len(mergeable_group)):
                    intersection = mergeable_group[g].intersection(grouplet)
                    if len(intersection) > 0:
                        mergeable_group[g] = mergeable_group[g].union(grouplet)
                        break
                else:
                    mergeable_group.append(grouplet)

            not_mergeables = set(range(trial_num)) - reduce(lambda x, y: x.union(y), mergeable_group, set())
            new_table.extend([self.trial_table[i] for i in not_mergeables])

            for group_index_set in mergeable_group:
                group_trial_list = sorted([self.trial_table[i] for i in group_index_set], key=lambda tri: tri.trial_range.start)
                merged = group_trial_list[0]
                for trial in group_trial_list[1:]:
                    merged = merged.merge(trial)
                new_table.append(merged)

            self.trial_table = sorted(new_table, key=lambda tri: tri.trial_range.start)
        if len(self.trial_table) > 0:
            self.current_max = self.trial_table[-1].trial_range.end()

    def suggest_next_trial(self, max_size: int) -> Trial:
        try:
            strategy = _TRIAL_SUGGEST[CONFIG.table.trial_suggest_method]
        except KeyError:
            raise ValueError("不正な suggest_method です %s" % CONFIG.table.trial_suggest_method.name)

        with self._table_lock:
            trial_range = strategy.suggest(max_size, self.trial_table)
            trial = Trial(
                self.study_id,
                Trial.create_trial_hash(self.study_id, trial_range),
                trial_range,
                self.target,
                self.method,
                TrialStatus.RESERVED
            )
            self.trial_table.append(trial)
        return trial

    def update_table(self, new_trial: Trial):
        with self._table_lock:
            for i in range(len(self.trial_table)):
                if self.trial_table[i].trial_id != new_trial.trial_id:
                    continue

                self.trial_table[i] = new_trial
                if new_trial.is_resolved():
                    self.result = new_trial.preimage

                break
            else:
                raise ValueError("不正な id です: %s" % new_trial.trial_id)

    def is_resolved(self) -> bool:
        return self.result is not None

    def to_dict(self) -> dict:
        if self.result is None:
            result = None
        else:
            result = to_hex(self.result)

        return {
                "study_id": self.study_id,
                "target": self.target,
                "method": self.method,
                "trial_table": [tri.to_dict() for tri in self.trial_table],
                "current_max": self.current_max,
                "result": result
            }

    @staticmethod
    def from_dict(d: dict) -> Study:
        target = from_hex(d["target"])
        prefix = from_hex(d["target"][0:12])
        study_id = str(uuid.uuid1(prefix))
        return Study(study_id, target, HashMethod(d["method"]), [])
