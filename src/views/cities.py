from pathlib import Path

from flasgger import swag_from
from flask import request
from flask_restful import Resource
from src.auth import authenticate
from src.constants import JSON_SCHEMA_PATH, SWAGGER_PATH
from src.services.cities import CityService
from src.utils import exception_handler
from src.validators import Validator


class City(Resource):
    CITY_SWAGGER_PATH = Path.joinpath(SWAGGER_PATH, "city")
    CITY_JSON_SCHEMA_PATH = Path.joinpath(JSON_SCHEMA_PATH, "city")

    @swag_from(Path.joinpath(CITY_SWAGGER_PATH, "get_cities.yml"))
    @exception_handler
    def get(self):
        return {"data": CityService().get_cities()}, 200

    @swag_from(Path.joinpath(CITY_SWAGGER_PATH, "create_city.yml"))
    @exception_handler
    @authenticate
    def post(self):
        file_path = Path.joinpath(self.CITY_JSON_SCHEMA_PATH, "create_city.json")
        validator = Validator(file_path, request.get_json())
        validation_error = validator.validate_request()
        if validation_error:
            return {"message": "Invalid Request: " + str(validation_error)}, 400
        return CityService().create_city(validator.data)
