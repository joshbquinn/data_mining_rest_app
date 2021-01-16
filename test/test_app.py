import unittest
import json

from rest_mediator import dataset_resource

BASE_URL = 'http://127.0.0.1:5000'
DATASET_PATH = '/datasets'
ALGORITHM_PATH = '/algorithms'
DATA_ANALYSIS_PATH = '/data-analysis/'


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = dataset_resource.app.test_client()
        self.app.testing = True

    def test_get_all_datasets(self):
        response = self.app.get(BASE_URL+DATASET_PATH)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['datasets']), 5)

    def test_get_one_dataset(self):
        expected_entry = {'index': 0, 'alcohol': 14.23, 'malic_acid': 1.71, 'ash': 2.43, 'alcalinity_of_ash': 15.6, 'magnesium': 127.0, 'total_phenols': 2.8, 'flavanoids': 3.06, 'nonflavanoid_phenols': 0.28, 'proanthocyanins': 2.29, 'color_intensity': 5.64, 'hue': 1.04, 'od280/od315_of_diluted_wines': 3.92, 'proline': 1065.0}
        response = self.app.get(BASE_URL+ DATASET_PATH + '?name=wine')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0], expected_entry)

    def test_dataset_not_exist(self):
        response = self.app.get(BASE_URL + DATASET_PATH + '/?name=unknown')
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # invalid: incorrect content-type application/json
        item = {"id": "1",
                "name": "test_dataset"}
        message = "Resource could not be created. " \
                  "Check the CSV file is in the correct format and " \
                  "is attached in 'form-data' parameter. " \
                  "Ensure the accept header is 'text/csv'."
        response = self.app.post(BASE_URL + DATASET_PATH,
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertIn(message,data['message'])

    def test_delete(self):
        response = self.app.delete(BASE_URL + DATASET_PATH + '/1')
        self.assertEqual(response.status_code, 204)

    def test_delete_non_existing_resource(self):
        expected_message = f"Dataset with id 6 does not exist."
        response = self.app.delete(BASE_URL + DATASET_PATH + '/6')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], expected_message)

    def test_get_algorithms(self):
        response = self.app.get(BASE_URL + ALGORITHM_PATH)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], '1')
        self.assertEqual(data['type'], 'linear regression')

    def test_get_analysis(self):
        algorithm = 'linear regression'
        dataset = 'boston_house_prices'
        independents = 'NOX,RM,AGE'
        dependent = 'MEDV'
        query_string = f'?algorithm={algorithm}&dataset={dataset}&independents={independents}&dependent={dependent}'
        expected_dep = 'Dep. Variable:                   MEDV'
        expected_r_sq = 'R-squared (uncentered):                   0.930'
        print(DATA_ANALYSIS_PATH + query_string)
        response = self.app.get(BASE_URL + DATA_ANALYSIS_PATH + query_string)
        data = str(response.get_data())
        self.assertIn(expected_dep, data)
        self.assertIn(expected_r_sq, data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()