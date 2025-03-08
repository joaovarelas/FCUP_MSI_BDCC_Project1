from flask import Flask, Blueprint, jsonify, request
from connectors import db



def get_admissions():
    result = list()
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM admissions")
        rows = cursor.fetchall()

        for row in rows:
            admission = {
                "admission_id": row[0],
                "patient_id": row[1],
                "doctor_id": row[2],
                "admit_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None,
                "discharge_time": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None,
                "admission_type": row[5],
                "diagnosis": row[6]
            }
            result.append(admission)
            if len(result) > 50:  # limit to top 50 rows
                break

            
    except Exception as e:
        return jsonify(error=f"Error fetching data: {e}"), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(admissions=result), 200

    

def get_admission_by_id(admission_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM admissions WHERE admission_id = %s", (admission_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify(error="Admission not found"), 404

        return jsonify(admission=row), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()



def add_admission(patient_id, doctor_id, admission_type, diagnosis, admit_time=None, discharge_time=None):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        # If admit_time is not provided, use the current timestamp
        if admit_time is None:
            admit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        insert_query = '''
        INSERT INTO admissions (patient_id, doctor_id, admit_time, discharge_time, admission_type, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (patient_id, doctor_id, admit_time, discharge_time, admission_type, diagnosis))
        connection.commit()
        return jsonify(message="Admission created successfully"), 201

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()



def update_admission(admission_id, patient_id=None, doctor_id=None, admission_type=None, diagnosis=None, discharge_time=None):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        update_query = "UPDATE admissions SET "
        values = []

        if patient_id:
            update_query += "patient_id = %s, "
            values.append(patient_id)
        if doctor_id:
            update_query += "doctor_id = %s, "
            values.append(doctor_id)
        if admission_type:
            update_query += "admission_type = %s, "
            values.append(admission_type)
        if diagnosis:
            update_query += "diagnosis = %s, "
            values.append(diagnosis)
        if discharge_time:
            update_query += "discharge_time = %s, "
            values.append(discharge_time)

        # Remove the trailing comma
        update_query = update_query.rstrip(', ')
        update_query += " WHERE admission_id = %s"
        values.append(admission_id)

        cursor.execute(update_query, tuple(values))
        
        if cursor.rowcount == 0:
            return jsonify(error="Admission not found"), 404

        connection.commit()
        return jsonify(message="Admission updated successfully"), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()


def delete_admission(admission_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        delete_query = "DELETE FROM admissions WHERE admission_id = %s"
        cursor.execute(delete_query, (admission_id,))

        if cursor.rowcount == 0:
            return jsonify(error="Admission not found"), 404

        connection.commit()
        return jsonify(message="Admission deleted successfully"), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()
