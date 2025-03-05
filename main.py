from flask import Flask, jsonify
from routes import patients

app = Flask(__name__)

# init routes flask REST API
app.register_blueprint(patients.patients_api)


@app.route('/')
def index():
    return jsonify(message="Big Data and Cloud Computing - FCUP")

if __name__ == '__main__':
    app.run(debug=True)
