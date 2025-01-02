import threading

from lite_dist.table_node.study import Study


_lock = threading.Lock()


class Curriculum:
    def __init__(self, studies: list[Study] | None = None):
        self.studies = studies or []

    def find_study(self, study_id: str) -> Study:
        for st in self.studies:
            if st.study_id != study_id:
                continue
            return st

        raise ValueError("不正な id です: %s" % study_id)

    def can_generate_trial(self) -> bool:
        for st in self.studies:
            if not st.is_resolved():
                return True
        return False

    def to_dict(self) -> dict:
        return {"studies": [st.to_dict(True) for st in self.studies]}

    def insert_study(self, study: Study):
        with _lock:
            self.studies.append(study)


CURRICULUM = Curriculum()
