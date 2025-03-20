from flask import Flask, jsonify
from routes import patient_route, admission_route, question_route, media_route, waitingtime_route, progress_route

app = Flask(__name__)

# init routes flask REST API
app.register_blueprint(patient_route.patient_api)
app.register_blueprint(admission_route.admission_api)
app.register_blueprint(question_route.question_api)
app.register_blueprint(media_route.media_api)
app.register_blueprint(waitingtime_route.waitingtime_api)
app.register_blueprint(progress_route.progress_api)



@app.route('/')
def index():
    return jsonify(message="Big Data and Cloud Computing - FCUP")

if __name__ == '__main__':
    app.run(debug=True)
