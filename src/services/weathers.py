import json
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import List


class WeatherService:
    @staticmethod
    def update_weathers_in_file(
        file_path: Path, file_date: date, from_datetime: datetime, to_datetime: datetime, temperature: int
    ) -> List[dict]:
        def get_weather(weather: dict) -> dict:
            file_time: time = datetime.strptime(weather["time"], "%H:%M:%S").time()
            file_datetime = datetime.combine(file_date, file_time)
            if from_datetime <= file_datetime <= to_datetime:
                weather.update({"temperature": temperature})
                _weather = weather.copy()
                _weather.update({"date": file_date.__str__()})
                return _weather

        with open(file_path, "r+") as file:
            if weathers := json.load(file):
                updated_weathers = list(filter(None, list(map(get_weather, weathers))))
                file.seek(0)
                json.dump(weathers, file, indent=4)
                return updated_weathers
            return []

    def update_weather(self, payload: dict):
        from_timestamp = payload.get("from_timestamp")
        to_timestamp = payload.get("to_timestamp")
        time_delta = to_timestamp - from_timestamp

        updated_weathers = []
        for i in range(time_delta.days + 1):
            file_date = (from_timestamp + timedelta(i)).date()
            file = Path.joinpath(payload.get("city_dir"), f"{file_date}.json")
            if file.exists():
                updated_weathers.extend(
                    self.update_weathers_in_file(
                        file, file_date, from_timestamp, to_timestamp, payload.get("temperature")
                    )
                )

        if updated_weathers:
            return {"data": updated_weathers}, 200

        message = "Weather details not found for city {} and {} in between {} timestamp".format(
            payload.get("city", {}).get("city"), from_timestamp, to_timestamp
        )
        return {"message": message}, 404

    def get_weathers(self, filters: dict):
        from_timestamp = filters.get("from_timestamp")
        to_timestamp = filters.get("to_timestamp")
        time_delta = to_timestamp - from_timestamp

        weathers = []
        for i in range(time_delta.days + 1):
            file_date = (from_timestamp + timedelta(i)).date()
            file = Path.joinpath(filters.get("city_dir"), f"{file_date}.json")
            if file.exists():
                # get data from file
                weathers.extend(self.get_weathers_from_file(file, file_date, from_timestamp, to_timestamp))
        return weathers

    @staticmethod
    def get_weathers_from_file(
        file_path: Path,
        file_date: date,
        from_datetime: datetime,
        to_datetime: datetime,
    ) -> List[dict]:
        def get_weather(weather: dict) -> dict:
            file_time: time = datetime.strptime(weather["time"], "%H:%M:%S").time()
            file_datetime = datetime.combine(file_date, file_time)
            if from_datetime <= file_datetime <= to_datetime:
                weather.update({"date": file_date.__str__()})
                return weather

        with open(file_path, "r+") as file:
            if weathers := json.load(file):
                return list(filter(None, list(map(get_weather, weathers))))
            return []

    def create_weather(self, payload: dict):
        timestamp = payload.get("timestamp")

        # create weather if not exists
        with open(payload.get("weather_file"), "r+") as file:
            weathers = json.load(file)

            # rais if weather and temperature details exists
            exists_weather = list(
                filter(
                    lambda weather: datetime.strptime(weather["time"], "%H:%M:%S").time()
                    == timestamp.time(),
                    weathers,
                )
            )
            if any(exists_weather):
                return {"message": "Weather info is already exists for given time"}, 409

            weather = {
                "time": timestamp.time().strftime("%H:%M:%S"),
                "temperature": payload.get("temperature"),
            }
            weathers.append(weather)
            file.seek(0)
            json.dump(weathers, file, indent=4)

        return weather, 201
