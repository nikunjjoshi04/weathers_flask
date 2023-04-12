from datetime import datetime
from pathlib import Path

from jsonschema.validators import validate
from src.utils import read_json


class Validator:
    def __init__(self, file_path: Path, data):
        self.file_path = file_path
        self.data = data
        self.strip_str()

    @property
    def json_schema(self):
        return read_json(self.file_path)

    def validate_request(self):
        try:
            validate(self.data, self.json_schema)
        except Exception as e:
            error_string = str(e.message)
            return error_string

    def validate_datetime(self, date_time):
        try:
            return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return False

    def strip_str(self):
        self.data.update({key: val.strip() for key, val in self.data.items() if isinstance(val, str)})
