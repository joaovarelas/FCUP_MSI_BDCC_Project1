from flask import Flask, Blueprint, jsonify, request
from connectors import db
from google.cloud import storage
import uuid
import datetime
import os 

#BUCKET_NAME = "bucket-patient-files"
BUCKET_NAME = os.getenv("BUCKET_NAME")


def get_media_by_patient(patient_id):
 
    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()  

        query = '''
        SELECT media_id, file_source, file_description, uploaded_at
        FROM media
        WHERE patient_id = %s
        '''
        cursor.execute(query, (patient_id,))
        media_records = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "patient_id": patient_id,
            "media": media_records
        }), 200

    except Exception as e:
        return jsonify(error=str(e)), 500




def generate_signed_url(file_uuid):

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        query = "SELECT file_source FROM media WHERE file_source = %s"
        cursor.execute(query, (file_uuid,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if not result:
            return jsonify(error="File not found"), 404

        # File exists, generate signed URL
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_uuid)

        # Check if the blob exists in Cloud Storage
        if not blob.exists():
            return jsonify(error="File not found in Cloud Storage"), 404

        signed_url = blob.generate_signed_url(
            expiration=datetime.timedelta(hours=1),
            method="GET"
        )

        return jsonify({
            "file_uuid": file_uuid,
            "signed_url": signed_url
        }), 200

    except Exception as e:
        return jsonify(error=str(e)), 500




def upload_media(patient_id, file, file_description):

    try:
        unique_filename = str(uuid.uuid4())  

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file, content_type=file.content_type)

        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO media (patient_id, file_source, file_description)
        VALUES (%s, %s, %s)
        '''
        
        cursor.execute(insert_query, (patient_id, unique_filename, file_description))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            "message": "File uploaded successfully",
            "file_key": unique_filename  
        }), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
