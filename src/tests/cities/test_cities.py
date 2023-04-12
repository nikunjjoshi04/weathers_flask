import pytest
from src.main import app


class TestCities:
    @pytest.fixture
    def create_body(self):
        return {"city": "city1", "country": "country1"}

    def test_get_cities_blank(self, headers_without_access_token: dict):
        response = app.test_client().get("/cities", headers=headers_without_access_token)
        data = response.get_json()
        assert response.status_code == 200
        assert data == {"data": []}

    def test_create_cities_unauthorised(self, create_body: dict, headers_without_access_token: dict):
        response = app.test_client().post("/cities", headers=headers_without_access_token, json=create_body)
        data = response.get_json()
        assert response.status_code == 401
        assert data
        assert data == {"message": "Unauthorized"}

    def test_create_cities_city_not_null(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"city": ""})
        response = app.test_client().post("/cities", headers=headers_with_access_token, json=_create_body)
        data = response.get_json()
        assert response.status_code == 400
        assert data
        assert data == {"message": "Invalid Request: '' is too short"}

    def test_create_cities_country_not_null(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"country": ""})
        response = app.test_client().post("/cities", headers=headers_with_access_token, json=_create_body)
        data = response.get_json()
        assert response.status_code == 400
        assert data
        assert data == {"message": "Invalid Request: '' is too short"}

    def test_create_city_first(self, create_body: dict, headers_with_access_token: dict):
        response = app.test_client().post("/cities", headers=headers_with_access_token, json=create_body)
        data = response.get_json()
        assert response.status_code == 201
        assert data
        assert data == {"id": 1}

    def test_create_cities_conflict(self, create_body: dict, headers_with_access_token: dict):
        response = app.test_client().post("/cities", headers=headers_with_access_token, json=create_body)
        data = response.get_json()
        assert response.status_code == 409
        assert data
        assert data == {"message": "City already exists"}

    def test_create_city_second(self, create_body: dict, headers_with_access_token: dict):
        _create_body = create_body.copy()
        _create_body.update({"city": "city2"})
        response = app.test_client().post("/cities", headers=headers_with_access_token, json=_create_body)
        data = response.get_json()
        assert response.status_code == 201
        assert data
        assert data == {"id": 2}

    def test_get_cities(self, headers_without_access_token: dict):
        response = app.test_client().get("/cities", headers=headers_without_access_token)
        data = response.get_json()
        assert response.status_code == 200
        assert data
        assert data["data"]
        assert len(data["data"]) == 2
