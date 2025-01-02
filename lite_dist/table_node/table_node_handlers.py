from flask import Flask, request, jsonify

from lite_dist.common.trial import Trial
from lite_dist.common.register_result import StudyRegisterResult, TrialRegisterResult
from lite_dist.table_node.study import Study
from lite_dist.table_node.curriculum import CURRICULUM

app = Flask("table_node")


@app.route("/")
def handle_ping():
    return "<h1>LiteDist</h1>", 200


@app.route("/status")
def handle_status():
    return jsonify(CURRICULUM.to_dict()), 200


@app.route("/trial/register", methods=["POST"])
def handle_trial_register():
    try:
        trial = Trial.from_dict(request.json)
        study = CURRICULUM.find_study(trial.study_id)
        study.update_table(trial)
    except (KeyError, ValueError) as e:
        resp = TrialRegisterResult(False, False, str(e))
        return jsonify(resp.to_dict()), 400

    resp = TrialRegisterResult(True, CURRICULUM.can_generate_trial())
    return jsonify(resp.to_dict()), 200


@app.route("/study/register", methods=["POST"])
def handle_study_register():
    try:
        study = Study.from_dict(request.json)
    except (KeyError, ValueError) as e:
        resp = StudyRegisterResult(False, None, "Invalid format: " + str(e))
        return jsonify(resp.to_dict()), 400

    CURRICULUM.insert_study(study)
    resp = StudyRegisterResult(True, study.study_id)
    return jsonify(resp.to_dict()), 200
