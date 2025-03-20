from flask import Flask, Blueprint, jsonify, request
from connectors import db
from google.cloud import storage
import uuid
import datetime


BUCKET_NAME = "bucket-patient-files"

def upload_media(patient_id):
 
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    unique_filename = f"{uuid.uuid4()}"

    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file, content_type=file.content_type)

        # valid for 1 hour
        signed_url = blob.generate_signed_url(
            expiration=datetime.timedelta(hours=1),
            method="GET"
        )

        return jsonify({
            "message": "File uploaded successfully",
            "file_url": signed_url,  
            "filename": unique_filename
        }), 200

    except Exception as e:
        return jsonify({"error": f"File upload failed: {e}"}), 500
