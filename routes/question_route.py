from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import patient_svc


question_api = Blueprint('question', __name__)



@question_api.route('/rest/patient/<int:patient_id>/question', methods=['POST'])
def ask_question_route(patient_id):
    try:
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()

        # Extract the question text
        question_text = data.get('question')

        if not question_text:
            return jsonify(error="Question text is required"), 400

        # Get the doctor_id (you might need to associate the patient with a specific doctor)
        doctor_id = data.get('doctor_id')

        if not doctor_id:
            return jsonify(error="Doctor ID is required"), 400

        # Call the service to submit the question
        result = patient_svc.ask_question(patient_id, doctor_id, question_text)
        return jsonify(result)
    except Exception as err:
        return jsonify({"error": str(err)}), 500


# falta resposta as questoes (PUT?)