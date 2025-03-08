from flask import Flask, Blueprint, jsonify, request
from connectors import db


def get_patients():

    result = list()

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()

        for row in rows:
            #print(row)
            result.append(row)
            if len(result) > 50: # limit to top 50 rows
                break

    except Exception as e:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()


    return result



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

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()



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
        return jsonify(message="Patient deleted successfully"), 200

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
            return jsonify(error="Patient not found"), 404

        connection.commit()
        return jsonify(message="Patient updated successfully"), 200

    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()


