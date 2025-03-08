from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import patient_svc


patient_api = Blueprint('patient', __name__)

@patient_api.route('/rest/patient', methods=['GET'])
def list_patients_route():
    try:
        list_of_patients = patient_svc.get_patients()
        return jsonify(patients=list_of_patients)
    except Exception as err:
        return jsonify({"error":str(err)})



@patient_api.route('/rest/patient', methods=['POST'])
def create_patient_route():

    try: 
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()
        gender = data.get('gender')
        dob = data.get('dob')

        if gender not in ['M', 'F']:
            return jsonify(error="Invalid gender. Must be 'M' or 'F'."), 400

        dob = datetime.strptime(dob, '%Y-%m-%d')  # Ensure the format is YYYY-MM-DD
    except ValueError:
        return jsonify(error="Invalid date of birth format. Use YYYY-MM-DD."), 400

    try:
        patient_svc.add_patient(gender, dob) 
        return jsonify(message="Patient created successfully")

    except Exception as err:
        return jsonify({"error":str(err)})




@patient_api.route('/rest/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient_route(patient_id):
    try:
        result = patient_svc.delete_patient(patient_id)
        return result
    except Exception as err:
        return jsonify(error=str(err)), 500




@patient_api.route('/rest/patient/<int:patient_id>', methods=['PUT'])
def update_patient_route(patient_id):
    try:
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        # Get the JSON data from the request
        data = request.get_json()

        # Check for required fields in the JSON body and pass them to the update function
        gender = data.get('gender')  # May be None if not provided
        dob = data.get('dob')        # May be None if not provided
        dod = data.get('dod')        # May be None if not provided

        # Validate the dob field, if it's provided
        if dob:
            try:
                # Try to parse dob into a datetime object to validate its format
                dob = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify(error="Date of birth (dob) must be in 'YYYY-MM-DD HH:MM:SS' format"), 400

        # Validate the dod field, if it's provided
        if dod:
            try:
                # Try to parse dod into a datetime object to validate its format
                dod = datetime.strptime(dod, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify(error="Date of death (dod) must be in 'YYYY-MM-DD HH:MM:SS' format"), 400

        
        # Call the update_patient function, passing only the values that are provided
        result = patient_svc.update_patient(
            patient_id,
            gender=gender,
            dob=dob,
            dod=dod
        )

        return result

    except Exception as err:
        return jsonify(error=str(err)), 500