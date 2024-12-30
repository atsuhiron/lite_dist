from flask import Flask, request, jsonify

from lite_dist.table_node.study import Study
from lite_dist.table_node.curriculum import CURRICULUM

app = Flask("table_node")


@app.route("/")
def handle_ping():
    return "<h1>LiteDist</h1>"


@app.route("/status")
def handle_status():
    return jsonify(CURRICULUM.to_dict()), 200


@app.route("/study/register", methods=["POST"])
def handle_study_register():
    try:
        study = Study.from_dict(request.json)
    except (KeyError, ValueError) as e:
        return jsonify({"success": False, "message": "Invalid format: " + str(e)}), 400

    CURRICULUM.insert_study(study)
    return jsonify({"success": True, "id": study.study_id}), 200
