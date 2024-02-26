import os
import random
import string

from datetime import timedelta


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))
    SQLALCHEMY_DATABASE_URI = "sqlite:///tasks.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = "mySecretKey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN"
    JWT_ACCESS_CSRF_FIELD_NAME = "csrf_token"
    JWT_CSRF_CHECK_FORM = True
