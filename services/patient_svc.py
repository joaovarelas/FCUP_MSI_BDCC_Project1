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
            print(row)
            result.append(row)
            if len(result) > 50: # limit to top 50 rows
                break

    except Exception as e:
        print(f"Error fetching data: {e}")
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