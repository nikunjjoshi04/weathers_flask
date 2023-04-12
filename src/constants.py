from pathlib import Path

DATA_PATH = Path.joinpath(Path(__file__).parent.parent, "data")
CITIES_PATH = Path.joinpath(DATA_PATH, "cities.json")
SWAGGER_PATH = Path.joinpath(Path(__file__).parent, "swagger")
JSON_SCHEMA_PATH = Path.joinpath(Path(__file__).parent, "json_schemas")
