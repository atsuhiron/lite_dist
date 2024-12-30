import dataclasses
from functools import reduce

from lite_dist.common.trial import Trial
from lite_dist.common.enums import HashMethod, TrialStatus


class Study:
    def __init__(self, study_id: str, target: int, method: HashMethod, trial_table: list[Trial]):
        self.study_id = study_id
        self.target = target
        self.method = method
        self.trial_table = trial_table

        self.current_order = 0

    def simplify_table(self):
        new_table: list[Trial] = []
        mergeables: dict[int, set[int]] = {}
        trial_num = len(self.trial_table)
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

        self.trial_table = new_table

    def to_dict(self, for_display: bool) -> dict:
        if for_display:
            return {
                "study_id": self.study_id,
                "target": self.target,
                "method": self.method,
                "current_order": self.current_order
            }
        return {
                "study_id": self.study_id,
                "target": self.target,
                "method": self.method,
                "trial_table": [tri.to_dict() for tri in self.trial_table],
                "current_order": self.current_order
            }
