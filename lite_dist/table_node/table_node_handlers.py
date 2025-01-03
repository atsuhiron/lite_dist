import logging

from flask import Flask, request, jsonify

from lite_dist.common.trial import Trial
from lite_dist.common.register_result import StudyRegisterResult, TrialRegisterResult
from lite_dist.table_node.study import Study
from lite_dist.table_node.curriculum import CURRICULUM

app = Flask("table_node")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/")
def handle_ping():
    return "<h1>LiteDist</h1>", 200


@app.route("/status")
def handle_status():
    return jsonify(CURRICULUM.to_dict()), 200


@app.route("/study")
def handle_study():
    try:
        study_id = request.args["study_id"]
    except KeyError as e:
        return jsonify({"message": f"{e} を指定してください"}), 400

    try:
        study = CURRICULUM.pop_study_if_resolved(study_id)
        if study is None:
            return jsonify({"message": "%s has not been resolved yet" % study_id}), 200
        else:
            return jsonify(study.to_dict()), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route("/trial/reserve")
def handle_trial_reserve():
    try:
        max_size = int(request.args["max_size"])
        worker_name = request.args["name"]
    except KeyError as e:
        return jsonify({"message": f"{e} を指定してください"}), 400

    study = CURRICULUM.find_current_study()
    if study is None:
        return jsonify(Trial.create_empty().to_dict()), 200

    trial = study.suggest_next_trial(max_size)
    logger.info("Reserve trial: sid=%s name=%s size_power2=%.2f" % (study.study_id, worker_name, trial.get_size_power()))
    return jsonify(trial.to_dict()), 200


@app.route("/trial/register", methods=["POST"])
def handle_trial_register():
    try:
        worker_name = request.args["name"]
        trial = Trial.from_dict(request.json)
        study = CURRICULUM.find_study(trial.study_id)
        study.update_table(trial)
    except (KeyError, ValueError) as e:
        resp = TrialRegisterResult(False, False, str(e))
        return jsonify(resp.to_dict()), 400

    study.simplify_table()
    resp = TrialRegisterResult(True, CURRICULUM.can_generate_trial())
    logger.info("Register trial: sid=%s name=%s" % (study.study_id, worker_name))
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
    logger.info("Register study: sid=%s" % study.study_id)
    return jsonify(resp.to_dict()), 200
