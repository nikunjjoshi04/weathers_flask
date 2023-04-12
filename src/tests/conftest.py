import shutil
from pathlib import Path

import pytest
from src.constants import CITIES_PATH, DATA_PATH
from src.utils import create_dir, create_json_file


@pytest.fixture(scope="session")
def startup() -> dict:
    if not Path(DATA_PATH).exists():
        create_dir(DATA_PATH)
    if not Path(CITIES_PATH).exists():
        create_json_file(CITIES_PATH)
    yield DATA_PATH
    shutil.rmtree(DATA_PATH)


@pytest.fixture(scope="session")
def headers_without_access_token(startup: str) -> dict:
    return {"Content-Type": "application/json"}


@pytest.fixture(scope="session")
def headers_with_access_token(startup: str) -> dict:
    return {"Content-Type": "application/json", "access_token": "bbe12450-8bef-4635-a372-f7fee909d1b9"}
