from flask import Flask, Blueprint, jsonify, request
from connectors import db


# Function to add a question from a patient
def ask_question(patient_id, doctor_id, question_text):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO questions (patient_id, doctor_id, question)
        VALUES (%s, %s, %s)
        '''
        cursor.execute(insert_query, (patient_id, doctor_id, question_text))
        connection.commit()
        
        return {"message": "Question submitted successfully."}, 201
    except Exception as err:
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# Function to get all questions asked by a patient
def get_patient_questions(patient_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        select_query = '''
        SELECT question_id, doctor_id, question, reply, question_date, reply_date
        FROM questions
        WHERE patient_id = %s
        '''
        cursor.execute(select_query, (patient_id,))
        rows = cursor.fetchall()

        questions = []
        for row in rows:
            questions.append({
                "question_id": row[0],
                "doctor_id": row[1],
                "question": row[2],
                "reply": row[3],
                "question_date": row[4].strftime('%Y-%m-%d %H:%M:%S'),
                "reply_date": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
            })
        
        return questions
    except Exception as err:
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()
