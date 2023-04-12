from urllib.parse import urlencode

import pytest
from src.main import app


class TestWeathers:
    @pytest.fixture
    def create_body(self):
        return {"temperature": 88, "timestamp": "2023-03-25 08:58:58"}

    @pytest.fixture
    def update_body(self):
        return {"temperature": 888, "from_timestamp": "2023-03-25 08:58:58", "to_timestamp": "2023-03-27 22:44:44"}

    @pytest.fixture
    def query_params(self):
        return {"from_timestamp": "2023-03-25 06:44:44", "to_timestamp": "2023-03-27 22:44:44"}

    def test_get_weathers_blank(self, headers_without_access_token: dict, query_params: dict):
        params = {"city_id": 1, "query_params": urlencode(query_params)}
        url = "/cities/{city_id}/weathers?{query_params}".format(**params)
        response = app.test_client().get(url, headers=headers_without_access_token)
        data = response.get_json()
        assert response.status_code == 200
        assert data == {"data": []}

    def test_get_weathers_city_not_found(self, headers_without_access_token: dict, query_params: dict):
        params = {"city_id": 88, "query_params": urlencode(query_params)}
        url = "/cities/{city_id}/weathers?{query_params}".format(**params)
        response = app.test_client().get(url, headers=headers_without_access_token)
        data = response.get_json()
        assert response.status_code == 404
        assert data == {"message": "City with Id 88 not found"}

    def test_create_weather_unauthorised(self, create_body: dict, headers_without_access_token: dict):
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_without_access_token, json=create_body
        )
        data = response.get_json()
        assert response.status_code == 401
        assert data
        assert data == {"message": "Unauthorized"}

    def test_create_weather_temperature_should_be_integer(
        self, create_body: dict, headers_with_access_token: dict
    ):
        _create_body = create_body.copy()
        _create_body.update({"temperature": "88N"})
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=_create_body
        )
        data = response.get_json()
        assert response.status_code == 400
        assert data
        assert data == {"message": "Invalid Request: '88N' is not of type 'integer'"}

    def test_create_weather_timestamp_not_null(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"timestamp": ""})
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=_create_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {"message": "Invalid Request: '' is too short"}

    def test_create_weather_invalid_timestamp(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"timestamp": "2023-03-25--06:44:44"})
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=_create_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {"message": "Invalid timestamp 2023-03-25--06:44:44"}

    def test_create_weather_city_not_found(self, create_body: dict, headers_with_access_token: dict):
        response = app.test_client().post(
            "/cities/88/weathers", headers=headers_with_access_token, json=create_body
        )
        data = response.get_json()
        assert response.status_code == 404
        assert data
        assert data == {"message": "City with Id 88 not found"}

    def test_create_weather_first(self, create_body: dict, headers_with_access_token: dict):
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=create_body
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data
        _data = {
            "temperature": create_body.get("temperature"),
            "time": create_body.get("timestamp").split(" ")[-1],
        }
        assert data == _data

    def test_create_weathers_conflict(self, create_body: dict, headers_with_access_token: dict):
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=create_body
        )
        data = response.get_json()
        assert response.status_code == 409
        assert data
        assert data == {"message": "Weather info is already exists for given time"}

    def test_create_weather_second(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"timestamp": "2023-03-26 08:58:58"})
        response = app.test_client().post(
            "/cities/1/weathers", headers=headers_with_access_token, json=_create_body
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data
        _data = {
            "temperature": _create_body.get("temperature"),
            "time": _create_body.get("timestamp").split(" ")[-1],
        }
        assert data == _data

    def test_get_weathers(self, headers_without_access_token: dict, query_params: dict):
        params = {"city_id": 1, "query_params": urlencode(query_params)}
        url = "/cities/{city_id}/weathers?{query_params}".format(**params)
        response = app.test_client().get(url, headers=headers_without_access_token)
        data = response.get_json()
        assert response.status_code == 200
        assert data
        assert data["data"]
        assert len(data["data"]) == 2

    def test_update_weather_unauthorised(self, update_body: dict, headers_without_access_token: dict):
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_without_access_token, json=update_body
        )
        data = response.get_json()
        assert response.status_code == 401
        assert data
        assert data == {"message": "Unauthorized"}

    def test_update_weather_temperature_should_be_integer(
            self, update_body: dict, headers_with_access_token: dict
    ):
        _update_body = update_body.copy()
        _update_body.update({"temperature": "88N"})
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=_update_body
        )
        data = response.get_json()
        assert response.status_code == 400
        assert data
        assert data == {"message": "Invalid Request: '88N' is not of type 'integer'"}

    def test_update_weather_from_timestamp_not_null(self, update_body: dict, headers_with_access_token: dict):
        _update_body = update_body.copy()
        _update_body.update({"from_timestamp": ""})
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=_update_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {"message": "Invalid Request: '' is too short"}

    def test_update_weather_invalid_from_timestamp(self, update_body: dict, headers_with_access_token: dict):
        _update_body = update_body.copy()
        _update_body.update({"from_timestamp": "2023-03-25--06:44:44"})
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=_update_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {'message': 'Invalid timestamp from_timestamp 2023-03-25--06:44:44 to_timestamp 2023-03-27 22:44:44'}

    def test_update_weather_to_timestamp_not_null(self, update_body: dict, headers_with_access_token: dict):
        _update_body = update_body.copy()
        _update_body.update({"to_timestamp": ""})
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=_update_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {"message": "Invalid Request: '' is too short"}

    def test_update_weather_invalid_to_timestamp(self, update_body: dict, headers_with_access_token: dict):
        _update_body = update_body.copy()
        _update_body.update({"to_timestamp": "2023-03-25--06:44:44"})
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=_update_body
        )
        data = response.get_json()
        assert data
        assert response.status_code == 400
        assert data == {'message': 'Invalid timestamp from_timestamp 2023-03-25 08:58:58 to_timestamp 2023-03-25--06:44:44'}

    def test_update_weather_city_not_found(self, update_body: dict, headers_with_access_token: dict):
        response = app.test_client().patch(
            "/cities/88/weathers", headers=headers_with_access_token, json=update_body
        )
        data = response.get_json()
        assert response.status_code == 404
        assert data
        assert data == {"message": "City with Id 88 not found"}

    def test_update_weather(self, update_body: dict, headers_with_access_token: dict):
        response = app.test_client().patch(
            "/cities/1/weathers", headers=headers_with_access_token, json=update_body
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data
        assert data["data"]
        assert len(data["data"]) == 2
        assert [True, True] == [True for x in data["data"] if x.get('temperature') == 888]
