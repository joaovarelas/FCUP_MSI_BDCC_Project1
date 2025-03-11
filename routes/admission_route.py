from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import admission_svc


admission_api = Blueprint('admission', __name__)

@admission_api.route('/rest/admission', methods=['GET'])
def list_admissions_route():
    try:
        
        result = admission_svc.get_admissions()
        return jsonify(admissions=result), 200
    except Exception as err:
        return jsonify(error=str(err)), 500

@admission_api.route('/rest/admission/<int:admission_id>', methods=['GET'])
def get_admission_route(admission_id):
    try:
        
        result = admission_svc.get_admission_by_id(admission_id)
        return jsonify(admissions=result)
    except Exception as err:
        return jsonify(error=str(err)), 500

@admission_api.route('/rest/admission', methods=['POST'])
def create_admission_route():
    try:
        
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        
        data = request.get_json()
        
        patient_id = data.get('patient_id')
        admission_type = data.get('admission_type')
        diagnosis = data.get('diagnosis')
        admit_time = data.get('admit_time')  
        discharge_time = data.get('discharge_time')  
        admission_location = data.get('admission_location')  
        discharge_location = data.get('discharge_location')  
        death_time = data.get('death_time')  
        insurance = data.get('insurance')  
        language = data.get('language')  
        religion = data.get('religion')  
        marital_status = data.get('marital_status')  
        ethnicity = data.get('ethnicity')  
        ed_reg_time = data.get('ed_reg_time')  
        ed_out_time = data.get('ed_out_time')  
        hospital_expire_flag = data.get('hospital_expire_flag', 0)  
        has_chartevents_data = data.get('has_chartevents_data', 0)  

        
        if not patient_id or not admission_type or not diagnosis:
            return jsonify(error="Missing required fields: patient_id, admission_type, or diagnosis"), 400

        
        new_admission_id = admission_svc.add_admission(
            patient_id, admission_type, diagnosis, admit_time, discharge_time, death_time,
            admission_location, discharge_location, insurance, language, religion,
            marital_status, ethnicity, ed_reg_time, ed_out_time, hospital_expire_flag, has_chartevents_data
        )

        
        return jsonify({
            "message": "Admission created successfully",
            "hadm_id": new_admission_id
        }), 201

    except Exception as err:
        
        return jsonify(error=str(err)), 500

@admission_api.route('/rest/admission/<int:hadm_id>', methods=['PUT'])
def update_admission_route(hadm_id):
    try:
        
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        

        data = request.get_json()
        
        patient_id = data.get('patient_id')
        admission_type = data.get('admission_type')
        diagnosis = data.get('diagnosis')
        discharge_time = data.get('discharge_time')  
        admit_time = data.get('admit_time')  
        admission_location = data.get('admission_location')  
        discharge_location = data.get('discharge_location')  
        insurance = data.get('insurance')  
        language = data.get('language')  
        religion = data.get('religion')  
        marital_status = data.get('marital_status')  
        ethnicity = data.get('ethnicity')  
        ed_reg_time = data.get('ed_reg_time')  
        ed_out_time = data.get('ed_out_time')  
        hospital_expire_flag = data.get('hospital_expire_flag')  
        has_chartevents_data = data.get('has_chartevents_data')  

        
        updated_admission_id = admission_svc.update_admission(
            hadm_id, patient_id, admission_type, diagnosis, admit_time, discharge_time, admission_location,
            discharge_location, insurance, language, religion, marital_status, ethnicity, ed_reg_time,
            ed_out_time, hospital_expire_flag, has_chartevents_data
        )

        return jsonify({
            "message": "Admission update successfully",
            "hadm_id": updated_admission_id
        }), 200
        
    except Exception as err:
        return jsonify(error=str(err)), 500

@admission_api.route('/rest/admission/<int:admission_id>', methods=['DELETE'])
def delete_admission_route(admission_id):
    try:
        result = admission_svc.delete_admission(admission_id)
        return result
    except Exception as err:
        return jsonify(error=str(err)), 500
