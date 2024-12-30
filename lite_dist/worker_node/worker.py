from lite_dist.common.trial import Trial
from lite_dist.worker_node.table_node_client import BaseTableNodeClient


class Worker:
    def __init__(self, table_node_client: BaseTableNodeClient):
        self.client = table_node_client

    def start(self):
        ping_ok = self.client.ping_table_server()
        print(ping_ok)
