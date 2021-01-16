# database.py
# python file to mock persistence for project.
# Have created global objects in order call data from anywhere in project.
import os

from sklearn import datasets
import pandas as pd
import numpy as np

from configuration import DATA_PATH


def init_data():
    global all_datasets, dataset_keys, all_algorithms
    all_algorithms = {}
    all_datasets = {}
    dataset_keys = {}
    create_data(all_datasets, dataset_keys, all_algorithms)
    if len(os.listdir(DATA_PATH)) != 0:
        files = os.listdir(DATA_PATH)
        for file in files:
            add_to_db(file, all_datasets, dataset_keys)


def create_data(all_data, dataset_keys, all_algorithms):

    # DATASETS
    diabetes_data = np.c_[datasets.load_diabetes().data, datasets.load_diabetes().target]
    diabetes_cols = np.append(datasets.load_diabetes().feature_names, "diabetes_progression")
    diabetes_df = pd.DataFrame(diabetes_data, columns=diabetes_cols)
    all_data["diabetes"] = diabetes_df
    dataset_keys[1] = "diabetes"

    boston_data = np.c_[datasets.load_boston().data, datasets.load_boston().target]
    boston_cols = np.append(datasets.load_boston().feature_names, 'MEDV')
    boston_df = pd.DataFrame(boston_data, columns=boston_cols)
    all_data["boston_house_prices"] = boston_df
    dataset_keys[2] = "boston_house_prices"

    wine = pd.DataFrame(datasets.load_wine().data, columns=datasets.load_wine().feature_names)
    all_data["wine"] = wine
    dataset_keys[3] = "wine"

    # ALGORITHMS
    all_algorithms['id'] = '1'
    all_algorithms['type'] = 'linear regression'


def add_to_db(filename, all_datasets, dataset_keys):
    csv_df = pd.read_csv(os.path.join(DATA_PATH, filename))
    all_datasets[filename.replace(".csv", "")] = csv_df
    dataset_keys[len(dataset_keys) + 1] = filename.replace(".csv", "")



