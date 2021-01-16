from configuration import DATA_PATH
import os
from persistence import database as db


def create_dataset(csv_file):
    try:
        filename = csv_file.filename
        if find_data_by_name(filename.replace(".csv", "")) is None:
            csv_file.save(os.path.join(DATA_PATH, csv_file.filename))
            db.add_to_db(filename, all_datasets=db.all_datasets, dataset_keys=db.dataset_keys)
            return True
        else:
            print("Dataset already exists in persistence")
            return False
    except IOError:
        print("I/O error")
        return False


def find_dataset(id, name):
    try:
        if name is not None:
            return find_data_by_name(name)
        if id is not None:
            id = int(id)
            return find_data_by_id(id)
    except Exception as e:
        print("Error while trying process request.", e)
        return e


def find_all_datasets_info(uri):
    all_data = []
    for id, name in db.dataset_keys.items():
        data = {}
        data["id"] = id
        data["name"] = name
        data["href"] = uri+f"?name={name}"
        all_data.append(data)
    return {"datasets": all_data}


def find_data_by_id(id):
    name = db.dataset_keys.get(id)
    return db.all_datasets.get(name)


def find_data_by_name(name):
    try:
        return db.all_datasets[name]
    except Exception as e:
        print("Dataset does not exist.", e)


def remove_csv(id):
    data = find_data_by_id(id)
    if data is not None:
        delete_data_by_id(id)
    else:
        return None


def delete_data_by_id(id):
    key = db.dataset_keys.get(id)
    del db.all_datasets[key]


def idbyname(name):
    return list(db.dataset_keys.keys())[list(db.dataset_keys.values()).index(name)]


def namebyid(id):
    return db.dataset_keys.get(id)


def find_number_of_dataset():
    return len(db.all_datasets)


def find_available_algorithms():
    return db.all_algorithms


def id_exists(id):
    name = namebyid(id)
    if name is None:
        return False
    else:
        return True
