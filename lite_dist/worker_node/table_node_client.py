import abc

import requests

from lite_dist.common.trial import Trial
from lite_dist.common.register_result import TrialRegisterResult
from lite_dist.worker_node.exceptions import RequestError


class BaseTableNodeClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ping_table_server(self) -> bool:
        pass

    @abc.abstractmethod
    def reserve_trial(self, max_size: int) -> Trial:
        pass

    @abc.abstractmethod
    def register_trial(self, trial: Trial) -> TrialRegisterResult:
        pass


class TableNodeClient(BaseTableNodeClient):
    def __init__(self, ip: str):
        self.domain = "http://" + ip

    def ping_table_server(self) -> bool:
        try:
            _ = self._ping()
            return True
        except RequestError:
            return False

    def reserve_trial(self, max_size: int) -> Trial:
        pass

    def register_trial(self, trial: Trial) -> TrialRegisterResult:
        pass

    def _ping(self, path: str = "/") -> str:
        resp = requests.get(self.domain + path)
        if resp.status_code != 200:
            raise RequestError("Request to %s is failed, status code is: %d" % (self.domain + path, resp.status_code))
        return resp.content.decode()

    def _post(self, path: str, body: dict[str, str]) -> dict:
        resp = requests.post(self.domain + path, data=body)
        if resp.status_code != 200:
            raise RequestError("Request to %s is failed, status code is: %d" % (self.domain + path, resp.status_code))
        return resp.json()
