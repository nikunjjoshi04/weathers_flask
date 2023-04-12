from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from loguru import logger
from src.constants import CITIES_PATH, DATA_PATH
from src.utils import create_dir, create_json_file
from src.views.cities import City
from src.views.weathers import Weather

app = Flask(__name__)
api = Api(app)

app.config["SWAGGER"] = {"title": "Weathers", "specs_route": "/"}
Swagger(app)


if not Path(DATA_PATH).exists():
    logger.info("Creating Data Dir...")
    create_dir(DATA_PATH)
if not Path(CITIES_PATH).exists():
    logger.info("Creating cities file...")
    create_json_file(CITIES_PATH)


api.add_resource(City, "/cities")
api.add_resource(Weather, "/cities/<int:city_id>/weathers")
