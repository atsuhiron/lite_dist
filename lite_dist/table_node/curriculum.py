from lite_dist.table_node.study import Study


class Curriculum:
    def __init__(self, studies: list[Study] | None = None):
        self.studies = studies or []

    def to_dict(self) -> dict:
        return {"studies": [st.to_dict(True) for st in self.studies]}


CURRICULUM = Curriculum()
