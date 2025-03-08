from flask import Flask, Blueprint, jsonify, request
from connectors import db


def get_patients(limit=50):
    result = []

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

    except Exception as e:
        raise Exception(str(e))
    finally:
        cursor.close()
        connection.close()

    return jsonify(result)


def add_patient(gender, dob):
    # Insert into the patients table
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO patients (gender, date_of_birth)
        VALUES (%s, %s)
        '''
        cursor.execute(insert_query, (gender, dob))
        connection.commit()

        new_patient_id = cursor.lastrowid  # Get the last inserted ID

    except Exception as err:
        raise Exception(str(err))
    finally:
        cursor.close()
        connection.close()

    return new_patient_id


def delete_patient(patient_id):
    # Delete a patient from the patients table
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        delete_query = """
        DELETE FROM patients WHERE patient_id = %s
        """
        cursor.execute(delete_query, (patient_id,))
        
        if cursor.rowcount == 0:
            return jsonify(error="Patient not found"), 404
        
        connection.commit()

        return jsonify({
            "message": "Patient deleted successfully",
            "patient_id": patient_id}), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()



def update_patient(patient_id, gender=None, dob=None, dod=None):
    # Update the patient details (gender, dob, dod) based on patient_id
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        # Start building the update query dynamically based on which fields are provided
        update_query = "UPDATE patients SET "
        values = []

        # Conditionally add the fields to be updated
        if gender:
            update_query += "gender = %s, "
            values.append(gender)
        if dob:
            update_query += "date_of_birth = %s, "
            values.append(dob)
        if dod is not None:  # This is checking for `None` because `dod` could be NULL.
            update_query += "date_of_death = %s, "
            values.append(dod)

        # Remove the last comma and space
        update_query = update_query.rstrip(', ')

        # Add the WHERE condition to specify which patient to update
        update_query += " WHERE patient_id = %s"
        values.append(patient_id)

        # Execute the update query
        cursor.execute(update_query, tuple(values))
        
        if cursor.rowcount == 0:
            return jsonify(error="Patient not found or not updated"), 404

        connection.commit()
        return jsonify({
            "message": "Patient updated successfully",
            "patient_id": patient_id}), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()


