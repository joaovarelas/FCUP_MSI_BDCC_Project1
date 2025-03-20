from flask import Flask, Blueprint, jsonify, request
from connectors import db


def get_patients(limit=50):
    result = list()

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM patients LIMIT %s", (limit,))
        rows = cursor.fetchall()

        for row in rows:
            result.append({
                "patient_id": row[0],
                "gender": row[1],
                "date_of_birth": row[2].strftime("%Y-%m-%d %H:%M:%S") if row[2] else None,
                "date_of_death": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None
            })

    except Exception as err:
        return jsonify(error=str(err)), 500    
    finally:
        cursor.close()
        connection.close()

    return jsonify(patients=result), 200



def get_patient_by_id(patient_id):
    result = {}

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        row = cursor.fetchone()
        
        if row:
            result = {
                "patient_id": row[0],
                "gender": row[1],
                "date_of_birth": row[2].strftime("%Y-%m-%d %H:%M:%S") if row[2] else None,
                "date_of_death": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None
            }
        else:
            return jsonify(error=f"Patient with ID {patient_id} not found."), 404

    except Exception as err:
        return jsonify(error=f"Error fetching patient by ID: {str(err)}"), 500
    
    finally:
        cursor.close()
        connection.close()

    return jsonify(patient=result), 200


def add_patient(gender, dob):
    
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO patients (gender, date_of_birth)
        VALUES (%s, %s)
        '''
        cursor.execute(insert_query, (gender, dob))
        connection.commit()

        new_patient_id = cursor.lastrowid  

    except Exception as err:
        return jsonify(error=str(err)), 500    
    finally:
        cursor.close()
        connection.close()

    return jsonify({
            "message": "Patient created successfully",
            "patient_id": new_patient_id}), 200  



def delete_patient(patient_id):
    
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        delete_query = """
        DELETE FROM patients WHERE patient_id = %s
        """
        cursor.execute(delete_query, (patient_id,))
        
        if cursor.rowcount == 0:
            raise Exception("Patient not found")
        
        connection.commit()

       
    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()

    return patient_id




def update_patient(patient_id, gender=None, dob=None, dod=None):
    
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()
        
        update_query = "UPDATE patients SET "
        values = []

        if gender:
            update_query += "gender = %s, "
            values.append(gender)
        if dob:
            update_query += "date_of_birth = %s, "
            values.append(dob)
        if dod is not None:  
            update_query += "date_of_death = %s, "
            values.append(dod)

        update_query = update_query.rstrip(', ')
        
        update_query += " WHERE patient_id = %s"
        values.append(patient_id)

        cursor.execute(update_query, tuple(values))
        
        if cursor.rowcount == 0:
            raise Exception("Patient not found or not updated")

        connection.commit()

    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()

    return patient_id
