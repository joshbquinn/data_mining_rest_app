from pathlib import Path


def get_project_root():
    return Path(__file__).parent

ROOT_PATH = get_project_root()
DATA_PATH = str(ROOT_PATH) + "\persistence\data"
