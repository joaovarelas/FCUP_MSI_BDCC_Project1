from flask import jsonify
from connectors import  db

def progress_by_id(patient_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()


        admission_query = """
            SELECT hadm_id, admit_time, discharge_time, diagnosis
            FROM admissions
            WHERE patient_id = %s
            ORDER BY admit_time ASC;
        """
        cursor.execute(admission_query, (patient_id,))
        admissions = cursor.fetchall()

        icu_query = """
            SELECT icustay_id, intime, outtime
            FROM icustays
            WHERE patient_id = %s
            ORDER BY intime ASC;
        """
        cursor.execute(icu_query, (patient_id,))
        icu_stays = cursor.fetchall()

        inputevents_query = """
            SELECT inputevent_id, start_time, end_time, order_description
            FROM inputevents
            WHERE patient_id = %s
            ORDER BY start_time ASC;
        """
        cursor.execute(inputevents_query, (patient_id,))
        inputevents = cursor.fetchall()

        labevents_query = """
            SELECT labevent_id, test_time,test_value, test_value_num, test_flag, test_unit
            FROM labevents
            WHERE patient_id = %s
            ORDER BY test_time ASC;
        """
        cursor.execute(labevents_query, (patient_id,))
        labevents = cursor.fetchall()

        progress = {
            'admissions': admissions,
            'icu_stays': icu_stays,
            'inputevents': inputevents,
            'labevents': labevents,
        }

        return jsonify(progress=progress), 200
    except Exception as err:
        return jsonify(error=str(err)), 500
