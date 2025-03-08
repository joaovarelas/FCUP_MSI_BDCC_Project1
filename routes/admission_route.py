from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import admission_svc


admission_api = Blueprint('admission', __name__)

@admission_api.route('/rest/admission', methods=['GET'])
def list_admissions_route():
    try:
        # Fetch the list of all admissions using the service
        admissions = admission_svc.get_admissions()
        return admissions
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission/<int:admission_id>', methods=['GET'])
def get_admission_route(admission_id):
    try:
        # Fetch a specific admission by admission_id
        admission = admission_svc.get_admission_by_id(admission_id)
        return admission
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission', methods=['POST'])
def create_admission_route():
    try:
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()

        # Extract required data for creating an admission
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        admission_type = data.get('admission_type')
        diagnosis = data.get('diagnosis')
        admit_time = data.get('admit_time')  # Optional
        discharge_time = data.get('discharge_time')  # Optional

        # Call the service to add an admission
        result = admission_svc.add_admission(patient_id, doctor_id, admission_type, diagnosis, admit_time, discharge_time)
        return result
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission/<int:admission_id>', methods=['PUT'])
def update_admission_route(admission_id):
    try:
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()

        # Extract the fields that may be updated
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        admission_type = data.get('admission_type')
        diagnosis = data.get('diagnosis')
        discharge_time = data.get('discharge_time')  # Optional

        # Call the service to update the admission
        result = admission_svc.update_admission(admission_id, patient_id, doctor_id, admission_type, diagnosis, discharge_time)
        return result
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission/<int:admission_id>', methods=['DELETE'])
def delete_admission_route(admission_id):
    try:
        # Call the service to delete an admission
        result = admission_svc.delete_admission(admission_id)
        return result
    except Exception as err:
        return jsonify({"error": str(err)}), 500
