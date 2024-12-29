from flask import Flask

app = Flask("table_node")


@app.route("/ping")
def handle_ping() -> dict[str, str]:
    return {"name": "LiteDist"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=80)
