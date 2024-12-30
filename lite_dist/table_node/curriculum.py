import threading

from lite_dist.table_node.study import Study


_lock = threading.Lock()


class Curriculum:
    def __init__(self, studies: list[Study] | None = None):
        self.studies = studies or []

    def to_dict(self) -> dict:
        return {"studies": [st.to_dict(True) for st in self.studies]}

    def insert_study(self, study: Study):
        with _lock:
            self.studies.append(study)


CURRICULUM = Curriculum()
