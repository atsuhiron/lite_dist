from lite_dist.config import CONFIG
from lite_dist.table_node.table_node_handlers import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=CONFIG.port)
