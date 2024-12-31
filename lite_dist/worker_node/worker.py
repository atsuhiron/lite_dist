from lite_dist.config import CONFIG
from lite_dist.worker_node.table_node_client import BaseTableNodeClient


class Worker:
    def __init__(self, table_node_client: BaseTableNodeClient):
        self.client = table_node_client

    def start(self):
        ping_ok = self.client.ping_table_server()
        if not ping_ok:
            print("Failed to connect to table node server.")
            return

        if CONFIG.worker.trial_size_ratio <= 0:
            tsr = 9999
        else:
            tsr = CONFIG.worker.trial_size_ratio

