from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import patient_svc

patient_api = Blueprint('patient', __name__)

@patient_api.route('/rest/patient', methods=['GET'])
def get_patients_route():
    try:
        return patient_svc.get_patients()
    except Exception as err:
        return jsonify(error=str(err)), 500

@patient_api.route('/rest/patient/<int:patient_id>', methods=['GET'])
def get_patient_by_id_route(patient_id):
    try:
        return patient_svc.get_patient_by_id(patient_id)
    except Exception as err:
        return jsonify(error=str(err)), 500


@patient_api.route('/rest/patient', methods=['POST'])
def create_patient_route():
    try: 
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()
        gender = data.get('gender')
        dob = data.get('dob')

        if gender not in ['M', 'F']:
            return jsonify(error="Invalid gender. Must be 'M' or 'F'."), 400
        
        dob = datetime.strptime(dob, '%Y-%m-%d')  
    
        return patient_svc.add_patient(gender, dob) 

    except Exception as err:
        return jsonify(error=str(err)), 500
    
    

@patient_api.route('/rest/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient_route(patient_id):
    try:
        deleted_patient_id = patient_svc.delete_patient(patient_id)
        return jsonify({
            "message": "Patient deleted successfully",
            "patient_id": deleted_patient_id}), 200

    except Exception as err:
        return jsonify(error=str(err)), 500

@patient_api.route('/rest/patient/<int:patient_id>', methods=['PUT'])
def update_patient_route(patient_id):
    try:
        
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()
        
        gender = data.get('gender')
        dob = data.get('date_of_birth') 
        dod = data.get('date_of_death') 

        
        if dob:
            try:          
                dob = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify(error="Date of birth (dob) must be in 'YYYY-MM-DD HH:MM:SS' format"), 400

        
        if dod:
            try:            
                dod = datetime.strptime(dod, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify(error="Date of death (dod) must be in 'YYYY-MM-DD HH:MM:SS' format"), 400

        
        
        updated_patient_id = patient_svc.update_patient(
            patient_id,
            gender=gender,
            dob=dob,
            dod=dod
        )

        return jsonify({
            "message": "Patient updated successfully",
            "patient_id": updated_patient_id}), 200

    except Exception as err:
        return jsonify(error=str(err)), 500