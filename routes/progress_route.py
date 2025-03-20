from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import progress_svc

progress_api = Blueprint('progress', __name__)


@progress_api.route('/rest/progress/<int:patient_id>', methods=['GET'])
def get_progress_patient(patient_id):
    try:
        return progress_svc.progress_by_id(patient_id)
    except Exception as err:
        return jsonify(error=str(err)), 500