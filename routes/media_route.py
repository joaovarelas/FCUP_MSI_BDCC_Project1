from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import media_svc

media_api = Blueprint('media', __name__)


@media_api.route('/rest/media', methods=['GET'])
def get_all_media():
    return jsonify(message="TODO"), 200




@media_api.route('/rest/media/<int:patient_id>', methods=['GET'])
def get_patient_media(patient_id):
    try:
        return media_svc.get_media_by_patient(patient_id)
    except Exception as err:
        return jsonify(error=str(err)), 500


@media_api.route('/rest/media/uuid/<file_uuid>', methods=['GET'])
def get_signed_url(file_uuid):
    try:
        return media_svc.generate_signed_url(file_uuid)
    except Exception as err:
        return jsonify(error=str(err)), 500




@media_api.route('/rest/media/<int:patient_id>', methods=['POST'])
def upload_patient_media(patient_id):
    try:

        if 'file' not in request.files:
            return jsonify(error="No file provided"), 400

        file = request.files['file']
        file_description = request.form.get("description")  

       
        #if file.filename == '':
        #    return jsonify(error="No selected file"), 400


        if not file_description:
            return jsonify(error="File description is required"), 400

        return media_svc.upload_media(patient_id, file, file_description)

    except Exception as err:
        return jsonify(error=str(err)), 500