from functools import wraps

from flask import request
from src.config import settings


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get("access_token"):
            return {"message": "Unauthorized"}, 401

        # access_token = ""
        if request.headers.get("access_token") != settings.api_key:
            return {"message": "Unauthorized"}, 401
        return func(*args, **kwargs)

    return wrapper
