from flask import Flask, Blueprint, jsonify, request
from connectors import db


def get_admissions(limit=50):
    result = []

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM admissions LIMIT %s", (limit,))
        rows = cursor.fetchall()

        for row in rows:
            admission = {
                "hadm_id": row[0],
                "patient_id": row[1],
                "admit_time": row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else None,
                "discharge_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None,
                "death_time": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None,
                "admission_type": row[5],
                "admission_location": row[6],
                "discharge_location": row[7],
                "insurance": row[8],
                "language": row[9],
                "religion": row[10],
                "marital_status": row[11],
                "ethnicity": row[12],
                "ed_reg_time": row[13].strftime('%Y-%m-%d %H:%M:%S') if row[13] else None,
                "ed_out_time": row[14].strftime('%Y-%m-%d %H:%M:%S') if row[14] else None,
                "diagnosis": row[15],
                "hospital_expire_flag": row[16],
                "has_chartevents_data": row[17]
            }
            result.append(admission)

    except Exception as e:
        raise Exception(str(e)) 

    finally:
        cursor.close()
        connection.close()

    return result 
    

def get_admission_by_id(hadm_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        result = []

        
        cursor.execute("SELECT * FROM admissions WHERE hadm_id = %s", (hadm_id,))
        row = cursor.fetchone()

        
        if not row:
            raise Exception("Admission not found")

        
        admission = {
            "hadm_id": row[0],
            "patient_id": row[1],
            "admit_time": row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else None,
            "discharge_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None,
            "death_time": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None,
            "admission_type": row[5],
            "admission_location": row[6],
            "discharge_location": row[7],
            "insurance": row[8],
            "language": row[9],
            "religion": row[10],
            "marital_status": row[11],
            "ethnicity": row[12],
            "ed_reg_time": row[13].strftime('%Y-%m-%d %H:%M:%S') if row[13] else None,
            "ed_out_time": row[14].strftime('%Y-%m-%d %H:%M:%S') if row[14] else None,
            "diagnosis": row[15],
            "hospital_expire_flag": row[16],
            "has_chartevents_data": row[17]
        }

        result.append(admission)
        return result

    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()


def add_admission(
    patient_id, admission_type, diagnosis,
    admit_time=None, discharge_time=None, death_time=None,
    admission_location=None, discharge_location=None, 
    insurance=None, language=None, religion=None, marital_status=None, 
    ethnicity=None, ed_reg_time=None, ed_out_time=None, 
    hospital_expire_flag=0, has_chartevents_data=0
):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        
        if admit_time is None:
            admit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
        insert_query = """
        INSERT INTO admissions (
            patient_id, admission_type, diagnosis, admit_time, discharge_time, admission_location,
            discharge_location, death_time, insurance, language, religion, marital_status, ethnicity, ed_reg_time,
            ed_out_time, hospital_expire_flag, has_chartevents_data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        
        insert_data = (
            patient_id, admission_type, diagnosis, admit_time, discharge_time, admission_location,
            discharge_location, death_time, insurance, language, religion, marital_status, ethnicity, ed_reg_time,
            ed_out_time, hospital_expire_flag, has_chartevents_data
        )

        cursor.execute(insert_query, insert_data)
        connection.commit()
        
        new_admission_id = cursor.lastrowid
        return new_admission_id

    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()
        
        
        
    
def update_admission(hadm_id, patient_id=None,  admission_type=None, diagnosis=None, admit_time=None,   discharge_time=None, admission_location=None, discharge_location=None, insurance=None, language=None, 
                     religion=None, marital_status=None, ethnicity=None, ed_reg_time=None, ed_out_time=None, 
                     hospital_expire_flag=None, has_chartevents_data=None):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()
        update_query = "UPDATE admissions SET "
        values = []

        
        if patient_id is not None:
            update_query += "patient_id = %s, "
            values.append(patient_id)
        if admission_type is not None:
            update_query += "admission_type = %s, "
            values.append(admission_type)
        if diagnosis is not None:
            update_query += "diagnosis = %s, "
            values.append(diagnosis)
        if discharge_time is not None:
            update_query += "discharge_time = %s, "
            values.append(discharge_time)
        if admit_time is not None:
            update_query += "admit_time = %s, "
            values.append(admit_time)
        if admission_location is not None:
            update_query += "admission_location = %s, "
            values.append(admission_location)
        if discharge_location is not None:
            update_query += "discharge_location = %s, "
            values.append(discharge_location)
        if insurance is not None:
            update_query += "insurance = %s, "
            values.append(insurance)
        if language is not None:
            update_query += "language = %s, "
            values.append(language)
        if religion is not None:
            update_query += "religion = %s, "
            values.append(religion)
        if marital_status is not None:
            update_query += "marital_status = %s, "
            values.append(marital_status)
        if ethnicity is not None:
            update_query += "ethnicity = %s, "
            values.append(ethnicity)
        if ed_reg_time is not None:
            update_query += "ed_reg_time = %s, "
            values.append(ed_reg_time)
        if ed_out_time is not None:
            update_query += "ed_out_time = %s, "
            values.append(ed_out_time)
        if hospital_expire_flag is not None:
            update_query += "hospital_expire_flag = %s, "
            values.append(hospital_expire_flag)
        if has_chartevents_data is not None:
            update_query += "has_chartevents_data = %s, "
            values.append(has_chartevents_data)

        
        update_query = update_query.rstrip(', ')

        
        update_query += " WHERE hadm_id = %s"
        values.append(hadm_id)

        
        cursor.execute(update_query, tuple(values))
        
        if cursor.rowcount == 0:
            raise Exception("Admission not found")

        
        connection.commit()

        return hadm_id
    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()
        
        
def delete_admission(admission_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        delete_query = "DELETE FROM admissions WHERE hadm_id = %s"
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
