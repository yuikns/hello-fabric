# -*- coding: utf-8 -*-

import os

from .utils import mkdirs


class BaseConfig(object):
    PROJECT = "hello"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    FLASK_THREADED = True

    MONGO_ADDRESS = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "test"
    MONGO_USER = ""
    MONGO_PASS = ""

    ES_ADDRESS = "localhost"
    ES_PORT = 9200

    LOG_FOLDER = os.path.join(PROJECT_ROOT, 'logs')
    mkdirs(LOG_FOLDER)


class DefaultConfig(BaseConfig):
    pass
