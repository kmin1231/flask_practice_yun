# -*- coding: utf-8 -*-
import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = json.loads(open('{}/config.json'.format(ROOT_DIR)).read())


class JsonConfig:
    @staticmethod
    def get_data(varname, value=None):
        return DATA.get(varname) or os.environ.get(varname) or value

    @staticmethod
    def set_data(key, value):
        DATA[key] = value
        with open('{}/config.json'.format(ROOT_DIR), 'w') as f:
            json.dump(DATA, f, indent=4)


# app config
class Config:
    ROOT_DIR = ROOT_DIR
    STATIC_DIR = '{0}/static'.format(ROOT_DIR)
    TEMPLATES_DIR = '{0}/templates'.format(ROOT_DIR)
    ERROR_CODE = {
        40000: 'Bad Request',
        41000: 'Gone',
        40300: 'Forbidden',
        40400: 'Not Found',
        50000: 'Internal Server Error',
    }

    APP_MODE_PRODUCTION = 'production'
    APP_MODE_DEVELOPMENT = 'development'
    APP_MODE_TESTING = 'testing'

    APP_MODE = JsonConfig.get_data('APP_MODE', APP_MODE_PRODUCTION)
    APP_HOST = JsonConfig.get_data('APP_HOST', '0.0.0.0')
    APP_PORT = int(JsonConfig.get_data('APP_PORT', 80))

    # MongoDB setting
    DB_USER_NAME = JsonConfig.get_data('DB_USER_NAME', '')
    DB_USER_PASSWD = JsonConfig.get_data('DB_USER_PASSWD', '')
    DB_HOST = JsonConfig.get_data('DB_HOST', 'localhost')
    DB_PORT = JsonConfig.get_data('DB_PORT', 27017)
    DB_NAME = JsonConfig.get_data('DB_NAME', 'flask')

    REDIS_HOST = JsonConfig.get_data('REDIS_HOST', 'localhost')
    REDIS_PASSWD = JsonConfig.get_data('REDIS_PASSWD')

    @staticmethod
    def from_app_mode():
        mode = {
            Config.APP_MODE_PRODUCTION: 'config.ProductionConfig',
            Config.APP_MODE_DEVELOPMENT: 'config.DevelopmentConfig',
            Config.APP_MODE_TESTING: 'config.TestingConfig',
        }
        return mode.get(Config.APP_MODE, mode[Config.APP_MODE_DEVELOPMENT])

    @staticmethod
    def database_url(dialect='mongodb'):
        if dialect == 'mongodb':
            return 'mongodb://{}:{}@{}/{}'.format(Config.DB_USER_NAME, Config.DB_USER_PASSWD, Config.DB_HOST, Config.DB_NAME)


# flask config
class FlaskConfig:
    SECRET_KEY = '9022b99ae34ae74ec06bbeac8653b6c98a6ff9ee66ac4f96'
    
    # MongoDB URI setting
    MONGO_URI = f"mongodb://{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    pass


class DevelopmentConfig(FlaskConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(FlaskConfig):
    TESTING = True
