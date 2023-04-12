import json
from pathlib import Path

from loguru import logger


def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file) or []
    except Exception as e:
        logger.error(str(e))
        return {"message": str(e)}, 400


def create_dir(path):
    try:
        Path(path).mkdir(exist_ok=True)
    except Exception as e:
        logger.error(str(e))
        return {"message": str(e)}, 400


def create_json_file(path):
    try:
        Path(path).touch()
        with open(path, "w") as outfile:
            json.dump([], outfile, indent=4)
    except Exception as e:
        logger.error(str(e))
        return {"message": str(e)}, 400


def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": f"Internal server error {str(e)}"}, 500

    return inner
