from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import media_svc

media_api = Blueprint('media', __name__)


@media_api.route('/rest/media', methods=['GET'])
def get_all_media():
    return jsonify(message="TODO"), 200




@media_api.route('/rest/media/<int:patient_id>', methods=['GET'])
def get_patient_media():
    return jsonify(message="TODO"), 200




@media_api.route('/rest/media/<int:patient_id>', methods=['POST'])
def upload_patient_media(patient_id):
    try:
        return media_svc.upload_media(patient_id)
    except Exception as err:
        return jsonify(error=str(err)), 500

