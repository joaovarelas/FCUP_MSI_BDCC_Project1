from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import question_svc


question_api = Blueprint('question', __name__)

@question_api.route('/rest/questions/<int:patient_id>', methods=['GET'])
def get_questions_route(patient_id):
    try:
        return question_svc.get_patient_questions(patient_id)
    
    except Exception as err:
        return jsonify(error=str(err)), 500


@question_api.route('/rest/questions/<int:patient_id>', methods=['POST'])
def ask_question_route(patient_id):
    try:
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400
        
        data = request.get_json()
        question_text = data.get('question')
        #doctor_id = data.get('doctor_id')

        if not question_text:
            return jsonify(error="Question text is required"), 400
        #if not doctor_id:
        #   return jsonify(error="Doctor ID is required"), 400

        return question_svc.ask_question(patient_id, question_text)
        
    except Exception as err:
        return jsonify(error=str(err)), 500

@question_api.route('/rest/questions/<int:patient_id>/question/<int:question_id>', methods=['PUT'])
def answer_question_route(patient_id, question_id):
    try:
        # Check if the request body is JSON
        if not request.is_json:
            return jsonify(error="Request must be in JSON format"), 400

        # Extract the doctor's ID from the header
        doctor_id = request.headers.get('X-Doctor-ID')
        if not doctor_id:
            return jsonify(error="Doctor ID (X-Doctor-ID header) is required - AUTHORIZATION"), 401

        data = request.get_json()
        answer_text = data.get('answer')

        if not answer_text:
            return jsonify(error="Answer text is required"), 400

        # Call the service function with the doctor_id for validation and answering the question
        return question_svc.answer_question(patient_id, question_id, answer_text, doctor_id)

         

    except Exception as err:
        return jsonify(error=str(err)), 500