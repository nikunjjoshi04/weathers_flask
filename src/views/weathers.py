from pathlib import Path

from flasgger import swag_from
from flask import request
from flask_restful import Resource
from src.auth import authenticate
from src.constants import DATA_PATH, JSON_SCHEMA_PATH, SWAGGER_PATH
from src.services.cities import CityService
from src.services.weathers import WeatherService
from src.utils import create_json_file, exception_handler
from src.validators import Validator


class Weather(Resource):
    WEATHER_SWAGGER_PATH = Path.joinpath(SWAGGER_PATH, "weather")
    WEATHER_JSON_SCHEMA_PATH = Path.joinpath(JSON_SCHEMA_PATH, "weather")

    @swag_from(Path.joinpath(WEATHER_SWAGGER_PATH, "get_weathers.yml"))
    @exception_handler
    def get(self, city_id):
        filters = request.args.to_dict()
        filters.update({"city_id": city_id})

        # validate payload
        file_path = Path.joinpath(self.WEATHER_JSON_SCHEMA_PATH, "get_weather.json")
        validator = Validator(file_path, filters)
        validation_error = validator.validate_request()
        if validation_error:
            return {"message": "Invalid Request: " + str(validation_error)}, 400

        # validate from_timestamp and to_timestamp
        filters = validator.data
        from_timestamp = validator.validate_datetime(filters.get("from_timestamp"))
        to_timestamp = validator.validate_datetime(filters.get("to_timestamp"))
        if not from_timestamp or not to_timestamp:
            message = "Invalid timestamp from_timestamp {} to_timestamp {}".format(
                filters.get("from_timestamp"), filters.get("to_timestamp")
            )
            return {"message": message}, 400
        if from_timestamp > to_timestamp:
            message = "from_timestamp {} should not be greater then to_timestamp {}".format(
                from_timestamp, to_timestamp
            )
            return {"message": message}, 400

        # get city
        city = CityService().get_city(filters.get("city_id"))
        if not city:
            return {"message": f"City with Id {city_id} not found"}, 404

        # check city dir
        city_dir_name = f'{city.get("city").lower()}_{city.get("country").lower()}'
        city_dir = Path.joinpath(DATA_PATH, city_dir_name)
        if not city_dir.is_dir() or not city_dir.exists():
            return {"message": f"Dir of city {city_dir_name} not found"}, 404

        filters.update(
            {
                "city": city,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "city_dir": city_dir,
            }
        )
        return {"data": WeatherService().get_weathers(filters) or []}, 200

    @swag_from(Path.joinpath(WEATHER_SWAGGER_PATH, "create_weather.yml"))
    @exception_handler
    @authenticate
    def post(self, city_id):
        payload = request.get_json()
        payload.update({"city_id": city_id})

        # validate payload
        file_path = Path.joinpath(self.WEATHER_JSON_SCHEMA_PATH, "create_weather.json")
        validator = Validator(file_path, payload)
        validation_error = validator.validate_request()
        if validation_error:
            return {"message": "Invalid Request: " + str(validation_error)}, 400

        # validate timestamp
        payload = validator.data
        timestamp = validator.validate_datetime(payload.get("timestamp"))
        if not timestamp:
            message = f"Invalid timestamp {payload.get('timestamp')}"
            return {"message": message}, 400

        # get city
        city = CityService().get_city(payload.get("city_id"))
        if not city:
            return {"message": f"City with Id {city_id} not found"}, 404

        # check city dir
        city_dir_name = f'{city.get("city").lower()}_{city.get("country").lower()}'
        city_dir = Path.joinpath(DATA_PATH, city_dir_name)
        if not city_dir.is_dir() or not city_dir.exists():
            return {"message": f"Dir of city {city_dir_name} not found"}, 404

        # check weather file is exists or not, if not exists then create one
        weather_file = Path.joinpath(city_dir, f"{timestamp.date()}.json")
        if not weather_file.exists():
            create_json_file(weather_file)

        payload.update(
            {"city": city, "city_dir": city_dir, "timestamp": timestamp, "weather_file": weather_file}
        )
        return WeatherService().create_weather(payload)

    @swag_from(Path.joinpath(WEATHER_SWAGGER_PATH, "update_weather.yml"))
    @exception_handler
    @authenticate
    def patch(self, city_id):
        payload = request.get_json()
        payload.update({"city_id": city_id})

        # validate payload
        file_path = Path.joinpath(self.WEATHER_JSON_SCHEMA_PATH, "update_weather.json")
        validator = Validator(file_path, payload)
        validation_error = validator.validate_request()
        if validation_error:
            return {"message": "Invalid Request: " + str(validation_error)}, 400

        # validate from_timestamp and to_timestamp
        payload = validator.data
        from_timestamp = validator.validate_datetime(payload.get("from_timestamp"))
        to_timestamp = validator.validate_datetime(payload.get("to_timestamp"))
        if not from_timestamp or not to_timestamp:
            message = "Invalid timestamp from_timestamp {} to_timestamp {}".format(
                payload.get("from_timestamp"), payload.get("to_timestamp")
            )
            return {"message": message}, 400
        if from_timestamp > to_timestamp:
            message = "from_timestamp {} should not be greater then to_timestamp {}".format(
                from_timestamp, to_timestamp
            )
            return {"message": message}, 400

        # get city
        city = CityService().get_city(payload.get("city_id"))
        if not city:
            return {"message": f"City with Id {city_id} not found"}, 404

        # check city dir
        city_dir_name = f'{city.get("city").lower()}_{city.get("country").lower()}'
        city_dir = Path.joinpath(DATA_PATH, city_dir_name)
        if not city_dir.is_dir() or not city_dir.exists():
            return {"message": f"Dir of city {city_dir_name} not found"}, 404

        payload.update(
            {
                "city": city,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "city_dir": city_dir,
            }
        )

        return WeatherService().update_weather(payload)
