gcloud functions deploy bdcc-get-times-faas \
  --runtime python312 \
  --source . \
  --entry-point get_times \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west1 \
  --set-env-vars DB_USER=root,DB_PASSWORD=x%npoJsENm/5b8tz,DB_NAME=hospital_db,CLOUD_SQL_CONNECTION_NAME=bdcc2025-451416:europe-west1:bdcc-proj1-mysql,CLOUD_DB_PRIVATE_IP=10.31.64.3
