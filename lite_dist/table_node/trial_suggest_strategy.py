import abc

from lite_dist.common.enums import TrialStatus
from lite_dist.common.trial import TrialRange, Trial


class BaseTrialSuggestStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def suggest(self, max_size: int, trial_table: list[Trial]) -> TrialRange:
        pass


class SequentialTrialSuggestStrategy(BaseTrialSuggestStrategy):
    def suggest(self, max_size: int, trial_table: list[Trial]) -> TrialRange:
        if len(trial_table) == 0:
            return TrialRange(0, max_size)

        next_start_value = max(tri.trial_range.end() + 1 for tri in trial_table if tri.status != TrialStatus.NOT_CALCULATED)
        return TrialRange(next_start_value, max_size)
