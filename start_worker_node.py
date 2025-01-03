import argparse

from lite_dist.worker_node.worker import Worker
from lite_dist.worker_node.table_node_client import TableNodeClient


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP of Table node", type=str)
    parser.add_argument("name", help="name of this worker node", type=str)
    args = parser.parse_args()

    worker = Worker(TableNodeClient(args.ip, args.name))
    worker.start()
