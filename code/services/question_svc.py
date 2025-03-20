from flask import Flask, Blueprint, jsonify, request
from datetime import datetime
from connectors import db



# Function to get all questions asked by a patient
def get_patient_questions(patient_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        select_query = '''
        SELECT question_id, patient_id, question, reply, question_date, reply_date
        FROM questions
        WHERE patient_id = %s
        '''
        cursor.execute(select_query, (patient_id,))
        rows = cursor.fetchall()

        questions = []
        for row in rows:
            questions.append({
                "question_id": row[0],
                "patient_id": row[1],
                "question": row[2],
                "reply": row[3],
                "question_date": row[4].strftime('%Y-%m-%d %H:%M:%S'),
                "reply_date": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
            })
        
        return jsonify(questions=questions), 200
    
    except Exception as err:
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()
        
        
# Function to add a question from a patient
def ask_question(patient_id, question_text):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()


        insert_query = """
            INSERT INTO questions (patient_id, question, question_date)
            VALUES (%s, %s, %s)
        """
        question_date = datetime.now()
        cursor.execute(insert_query, (patient_id, question_text, question_date))

        connection.commit()
        question_id = cursor.lastrowid  # Get the ID of the inserted question

        return  jsonify({"message": "Question submitted successfully", 
                         "question_id": question_id}), 200
    
    except Exception as err:
        return jsonify(error=str(err)), 500
    
    finally:
        cursor.close()
        connection.close()


def answer_question(patient_id, question_id, reply_text, doctor_id):
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        # Check if the question exists and if it's already answered
        cursor.execute("SELECT question_id, reply FROM questions WHERE question_id = %s", (question_id,))
        question = cursor.fetchone()

        if not question:
            return jsonify(error="Question not found"), 404
        
        if question[1] is not None:  # Check if the reply is already set
            return jsonify(error="Question has already been answered"), 403

        # Check if the doctor (caregiver) treated this patient (check inputevents and labevents tables)
        cursor.execute("""
            SELECT caregiver_id 
            FROM inputevents 
            WHERE patient_id = %s AND caregiver_id = %s
        """, (patient_id, doctor_id,))

        caregiver_check = cursor.fetchone()

        if not caregiver_check:
            return jsonify(error="Doctor is not authorized to answer this patient's question"), 403

        # Update the question with the provided reply
        update_query = """
            UPDATE questions 
            SET reply = %s, reply_date = %s 
            WHERE question_id = %s
        """
        reply_date = datetime.now()
        cursor.execute(update_query, (reply_text, reply_date, question_id))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify(message="Reply submitted successfully"), 200
    
    except Exception as e:
        return jsonify(error=str(e)), 500