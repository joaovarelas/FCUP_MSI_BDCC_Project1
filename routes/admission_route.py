from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import admission_svc


admission_api = Blueprint('admission', __name__)

@admission_api.route('/rest/admission', methods=['GET'])
def list_admissions_route():
    try:
        # Fetch the list of all admissions using the service
        result = admission_svc.get_admissions()
        return jsonify(result)
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission/<int:admission_id>', methods=['GET'])
def get_admission_route(admission_id):
    try:
        # Fetch a specific admission by admission_id
        result = admission_svc.get_admission_by_id(admission_id)
        return result
    except Exception as err:
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission', methods=['POST'])
def create_admission_route():
    try:
        # Check if the request body is in JSON format
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        # Extract data from the JSON payload
        data = request.get_json()

        # Extract necessary fields for creating an admission
        patient_id = data.get('patient_id')
        admission_type = data.get('admission_type')
        diagnosis = data.get('diagnosis')
        admit_time = data.get('admit_time')  # Optional
        discharge_time = data.get('discharge_time')  # Optional
        admission_location = data.get('admission_location')  # Optional
        discharge_location = data.get('discharge_location')  # Optional
        insurance = data.get('insurance')  # Optional
        language = data.get('language')  # Optional
        religion = data.get('religion')  # Optional
        marital_status = data.get('marital_status')  # Optional
        ethnicity = data.get('ethnicity')  # Optional
        ed_reg_time = data.get('ed_reg_time')  # Optional
        ed_out_time = data.get('ed_out_time')  # Optional
        hospital_expire_flag = data.get('hospital_expire_flag', 0)  # Optional (default to 0)
        has_chartevents_data = data.get('has_chartevents_data', 0)  # Optional (default to 0)

        # Validation for required fields
        if not patient_id or not admission_type or not diagnosis:
            return jsonify(error="Missing required fields: patient_id, admission_type, or diagnosis"), 400

        # Call the service function to insert into the database
        admission_data = admission_svc.add_admission(
            patient_id, admission_type, diagnosis, admit_time, discharge_time,
            admission_location, discharge_location, insurance, language, religion,
            marital_status, ethnicity, ed_reg_time, ed_out_time, hospital_expire_flag,
            has_chartevents_data
        )

        # Return the response with the admission data (including `hadm_id`)
        return jsonify({
            "message": "Admission created successfully",
            "hadm_id": admission_data['hadm_id']
        }), 201

    except Exception as err:
        # Return any unexpected errors as a JSON response
        return jsonify({"error": str(err)}), 500



@admission_api.route('/rest/admission/<int:hadm_id>', methods=['PUT'])
def update_admission_route(hadm_id):
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
        result = admission_svc.update_admission(hadm_id, patient_id, doctor_id, admission_type, diagnosis, discharge_time)
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
