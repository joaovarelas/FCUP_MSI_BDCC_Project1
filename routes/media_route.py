from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
#from services import patient_svc

media_api = Blueprint('media', __name__)


@media_api.route('/rest/media', methods=['GET'])
def get_all_media():
    return jsonify(message="TODO12312312312"), 200


@media_api.route('/rest/media/<int:patient_id>', methods=['GET'])
def get_patient_media():
    return jsonify(message="TODO"), 200
