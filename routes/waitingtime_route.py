from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from services import waitingtime_svc

waitingtime_api = Blueprint('waitingtime', __name__)

@waitingtime_api.route('/rest/waitingtime', methods=['GET'])
def get_all_times():
    try:
        return waitingtime_svc.get_times()
    except Exception as err:
        return jsonify(error=str(err)), 500