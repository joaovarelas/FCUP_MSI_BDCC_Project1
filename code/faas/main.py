import os
import pymysql
from google.cloud.sql.connector import Connector, IPTypes
import functions_framework
from flask import jsonify
from datetime import datetime


def connect_to_cloud_sql():
    """Establish connection to Cloud SQL."""
    connector = Connector()

    instance_connection_name = os.getenv('CLOUD_SQL_CONNECTION_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    conn = connector.connect(
        instance_connection_name,  # Cloud SQL connection name
        "pymysql",                  # Using pymysql for MySQL
        user=db_user,               # Database username
        password=db_password,       # Database password
        db=db_name,                 # Database name
        ip_type=IPTypes.PRIVATE     # PRIVATE IP, CONNECT THROUGH VPC SERVERLESS ACCESS
    )
    return conn



@functions_framework.http
def get_times(request):
    limit = 50
    try:
        limit = int(request.args.get('limit', limit))
    except ValueError:
        return "Invalid limit value, it should be an integer.", 400

    result = []
    connection = None
    cursor = None

    connection = connect_to_cloud_sql()
    cursor = connection.cursor()

    cursor.execute("SELECT i.hadm_id , a.patient_id, a.admit_time, i.intime FROM admissions a inner join icustays i on a.hadm_id=i.hadm_id")
    data = cursor.fetchall()

    for row in data:
        admission_time = row[2]
        icu_entrance_time = row[3]

        waiting_time = (icu_entrance_time - admission_time).total_seconds() / 60  # in minutes

        result.append({
            "patient_id": row[1],
            "admission_time": admission_time.strftime("%Y-%m-%d %H:%M:%S"),
            "icu_entrance_time": icu_entrance_time.strftime("%Y-%m-%d %H:%M:%S"),
            "waiting_time": waiting_time
        })

    result.sort(key=lambda x: x["waiting_time"], reverse=True)
    final = result[:limit]


    cursor.close()

    connection.close()

    return jsonify(times=final), 200
