from flask import Flask, request, jsonify

app = Flask(__name__)

# I need to understand better the concept of the routes

@app.route('/', methods=['POST'])
def CreateProject():
    input_data = request.get_json()
    user_id = input_data.get('user_id')
    project_type = input_data.get('project_type')
    project_name = input_data.get('project_name')
    return jsonify({'projectId': 'uuid', 'projectType': project_type, 'projectName': project_name}), 200

@app.route('/', methods=['POST'])
def CreateDatasets():
    input_data = request.get_json()
    project_id = input_data.get('projectId')
    dataset_type = input_data.get('datasetType')
    dataset_name = input_data.get('datasetName')
    return jsonify({'datasetId': 'uuid', 'projectId': project_id, 'datasetType': dataset_type, 'datasetName': dataset_name}), 200

@app.route('/', methods=['POST'])
def StartTraining():
    input_data = request.get_json()
    dataset_id = input_data.get('datasetId')
    training_parameters = input_data.get('trainingParameters')
    return jsonify({'trainingJobId': 'uuid'}), 200

@app.route('/', methods=['GET'])
def StatusTraining():
    input_data = request.get_json()
    training_job_id = input_data.get('trainingJobId')
    return jsonify({'trainingJobId': training_job_id, 'trainingJobStatus': 'status_here'}), 200

@app.route('/', methods=['POST'])
def StopTraining():
    input_data = request.get_json()
    training_job_id = input_data.get('trainingJobId')
    return jsonify({'trainingJobId': training_job_id}), 200

@app.route('/', methods=['GET'])
def ResultsTraining():
    input_data = request.get_json()
    training_job_id = input_data.get('trainingJobId')
    return jsonify({'trainingJobId': training_job_id, 'trainingJobStats': 'stats_here', 'trainedModelId': 'model_id'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
