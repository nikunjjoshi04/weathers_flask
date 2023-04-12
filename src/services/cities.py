import json
from pathlib import Path
from typing import List

from src.constants import CITIES_PATH, DATA_PATH
from src.utils import read_json


class CityService:
    def get_cities(self) -> List[dict]:
        return read_json(CITIES_PATH)

    def get_city(self, city_id: int) -> dict:
        if cities := self.get_cities():
            if city := list(filter(lambda x: x.get("id") == city_id, cities)):
                return city[0]

    def create_city(self, city: dict) -> tuple:
        with open(CITIES_PATH, "r+") as file:
            cities = json.load(file)

            # check city is exists or not
            if any(
                list(
                    filter(
                        lambda x: x.get("city") == city.get("city")
                        and x.get("country") == city.get("country"),
                        cities,
                    )
                )
            ):
                return {"message": "City already exists"}, 409

            # create city dir in data dir
            city_dir_name = f'{city.get("city").lower()}_{city.get("country").lower()}'
            city_dir_path = Path.joinpath(DATA_PATH, city_dir_name)
            Path(city_dir_path).mkdir(exist_ok=True)

            # get auto incremented city id
            city_id = (cities[-1]["id"] + 1) if cities and cities[-1].get("id") else 1

            city.update({"id": city_id})
            cities.append(city)
            file.seek(0)
            json.dump(cities, file, indent=4)
            return {"id": city_id}, 201
