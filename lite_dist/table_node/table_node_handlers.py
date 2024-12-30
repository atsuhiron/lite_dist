from flask import Flask

from lite_dist.config import CONFIG
from lite_dist.table_node.curriculum import CURRICULUM

app = Flask("table_node")


@app.route("/")
def handle_ping() -> str:
    return "<h1>LiteDist</h1>"


@app.route("/status")
def handle_status() -> dict:
    return CURRICULUM.to_dict()
