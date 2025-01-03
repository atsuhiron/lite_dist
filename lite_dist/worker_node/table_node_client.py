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
    def __init__(self, ip: str, name: str):
        self.domain = "http://" + ip
        self.name = name

    def ping_table_server(self) -> bool:
        try:
            _ = self._get("/", resp_content_type="text")
            return True
        except RequestError:
            return False

    def reserve_trial(self, max_size: int) -> Trial:
        resp = self._get("/trial/reserve", {"max_size": str(max_size), "name": self.name})
        return Trial.from_dict(resp)

    def register_trial(self, trial: Trial) -> TrialRegisterResult:
        resp = self._post("/trial/register", trial.to_dict(), {"name": self.name})
        return TrialRegisterResult.from_dict(resp)

    def _get(self, path: str, param: dict[str, str] = None, resp_content_type: str = "json") -> str | dict:
        resp = requests.get(self.domain + path, param)
        if resp.status_code != 200:
            raise RequestError("Request to %s is failed, status code is: %d" % (self.domain + path, resp.status_code))

        if resp_content_type == "text":
            return resp.content.decode()
        if resp_content_type == "json":
            return resp.json()
        raise RequestError("不明な content_type です: %s" % resp_content_type)

    def _post(self, path: str, param: dict[str, str], body: dict) -> dict:
        resp = requests.post(self.domain + path, data=body, params=param)
        if resp.status_code != 200:
            raise RequestError("Request to %s is failed, status code is: %d" % (self.domain + path, resp.status_code))
        return resp.json()
