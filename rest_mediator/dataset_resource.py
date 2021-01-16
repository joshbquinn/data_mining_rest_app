from persistence import database

database.init_data()

from flask import Flask, request, Response
from data_processor import data_mining_processor as datamine
from persistence import csv_persistence as cp

import json

app = Flask(__name__)


def exception_response(error, message='Error processing request.', status=400, href=None):
    error = str(error)
    if href is None:
        return Response(response=json.dumps({'message': message, 'error': error, 'status': status}), status=400,
                        mimetype='application/json')
    elif href is not None:
        return Response(response=json.dumps({'message': message, 'error': error, 'status': status, 'href': href}),
                        status=400,
                        mimetype='application/json')


@app.route('/datasets', methods=['POST'])
def create_dataset():
    try:
        if request.accept_mimetypes['text/csv']:
            csv = request.files['file']
            if cp.create_dataset(csv) is True:
                id = cp.find_number_of_dataset()
                message = "Resource created successfully."
                response = Response(response=json.dumps({'message': message}),
                                    status=201, mimetype='application/json',
                                    headers={'Location': '/datasets?id=' + str(id)})
                response.headers['Dataset'] = cp.find_data_by_id(id)
                return response
            else:
                message = "Resource could not be created as it already exists."
                id = cp.idbyname(csv.filename.replace(".csv", ""))
                body = json.dumps(
                    {'message': message, 'dataset': csv.filename.replace(".csv", ""),
                     'href': f'<{request.url}?id={id}'})
                response = Response(response=body, status=303, mimetype='application/json')
                response.headers["Location"] = '/datasets?id=' + str(id)
                return response
        else:
            message = "Resource could not be created. " \
                      "Check the CSV file is in the correct format and " \
                      "is attached in 'form-data' parameter. " \
                      "Ensure the accept header is 'text/csv'."
            error = "Request Error"
            return exception_response(error=error, message=message)
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


@app.route('/datasets', methods=['GET'])
def get_dataset():
    try:
        if len(request.args) == 0:
            return get_all_datasets()
        id = request.args.get('id')
        name = request.args.get('name')
        dataset = cp.find_dataset(id, name)
        if dataset is not None:
            if id is None:
                id = cp.idbyname(name)
            id = int(id)
            response_data = dataset.to_json(orient='table')
            response = Response(response=response_data, status=200, mimetype='application/json',
                                headers={'Location': f"{request.path}?id={id}"})
            response.headers['Dataset'] = cp.namebyid(id)
            if id == cp.find_number_of_dataset():
                response.headers['Link'] = f"<{request.base_url}?id={id}>; rel='last'"
            else:
                response.headers['Link'] = f"<{request.base_url}?id={id + 1}>; rel='next'"
            return response
        else:
            message = f"No data could be found for 'id': {id} or 'name' {name}. " \
                      f"Ensure the correct ID or name for the dataset exists. " \
                      f"See '/datasets' to view available datasets."
            if dataset == type(Exception):
                e = dataset
            else:
                e = "GET dataset error."
            return exception_response(error=e, message=message, href=f"{request.url}")
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


def get_all_datasets():
    try:
        response_data = cp.find_all_datasets_info(request.url)
        response = Response(response=json.dumps(response_data), status=200, mimetype='application/json')
        return response
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


@app.route('/datasets/<id>', methods=['DELETE'])
def delete_dataset(id):
    try:
        id = int(id)
        if cp.id_exists(id) is True:
            cp.remove_csv(id)
            message = f'Deleted csv with {id}, there are {cp.find_number_of_dataset()} datasets in the database.'
            return Response(response=json.dumps({'message': message}), status=204, mimetype='application/json')
        else:
            message = f"Dataset with id {id} does not exist."
            return Response(response=json.dumps({'message': message, 'error': 'Datasource error', 'status': 404}), status=404)
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


@app.route('/algorithms', methods=['GET'])
def get_available_algorithms():
    try:
        algorithms = cp.find_available_algorithms()
        response_data = json.dumps(algorithms)
        response = Response(response=response_data, status=200, mimetype='application/json',
                            headers={'Location': '/algorithms'})
        return response
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


@app.route('/data-analysis/', methods=['GET'])
def get_data_analysis():
    try:
        algorithm_config = {}
        algorithm_name = request.args.get("algorithm")
        dataset_name = request.args.get("dataset")
        algorithm_config["independents"] = request.args.get("independents").split(",")
        algorithm_config["dependent"] = request.args.get("dependent")

        if algorithm_name is None or dataset_name is None or len(algorithm_config.values()) == 0:
            message = 'Query parameters "dataset" and "algorithm" must be present in URI.'
            return exception_response(error="Algorithm execution error.", message=message)
        else:
            dataset = cp.find_data_by_name(dataset_name)
            analysis = datamine.run(dataset, algorithm_config, algorithm_name)
            response = Response(response=str(analysis), status=200, mimetype='text/plain',
                                headers={'Location': '/run-algorithm'})
            return response
    except Exception as e:
        print("Error while trying process request.", e)
        return exception_response(e)


if __name__ == '__main__':
    app.run()
