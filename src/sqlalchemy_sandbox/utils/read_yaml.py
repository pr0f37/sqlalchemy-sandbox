import os
from pathlib import Path

import yaml


def find_file(current_path: Path, file_name: str) -> Path:
    file = Path(os.path.join(current_path, file_name))
    while not file.exists():
        path = Path(os.path.dirname(file)).parent
        if path == Path(os.getcwd()).parent:
            raise FileNotFoundError(file_name)
        file = Path(os.path.join(path, file_name))
    return file


def read_yaml_file(file: Path) -> dict:
    with open(file, "r") as f:
        return yaml.safe_load(f)
