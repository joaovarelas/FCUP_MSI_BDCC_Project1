from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import patient_svc


patients_api = Blueprint('patients', __name__)

@patients_api.route('/rest/patients', methods=['GET'])
def list_patients():
    try:
        list_of_patients = patient_svc.get_patients()
        return jsonify(patients=list_of_patients)
    except Exception as err:
        return jsonify({"error":str(err)})





@patients_api.route('/rest/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    gender = data.get('gender')
    dob = data.get('dob')
    if gender not in ['M', 'F']:
        return jsonify(error="Invalid gender. Must be 'M' or 'F'."), 400
    try:
        dob = datetime.strptime(dob, '%Y-%m-%d')  # Ensure the format is YYYY-MM-DD
    except ValueError:
        return jsonify(error="Invalid date of birth format. Use YYYY-MM-DD."), 400

    try:
        patient_svc.add_patient(gender, dob) 
        return jsonify(message="Patient created successfully")

    except Exception as err:
        return jsonify({"error":str(err)})






@patients_api.route('/rest/users/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    return jsonify(message="Patient deleted successfully")

@patients_api.route('/rest/users/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    return jsonify(message="Patient updated successfully")

