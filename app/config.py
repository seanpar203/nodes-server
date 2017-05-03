""" Module to handle different settings for different environments. """
from os import environ
from os.path import abspath, dirname

BASE_DIR = abspath(dirname(__file__))


class Config:
    """ Base configuration class that provide attrs unique to certain envs """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """ Production settings class, inherits from Config. """
    DEBUG = False


class StageConfig(Config):
    """ Staging settings class, inherits from Config. """
    DEBUG = True
    DEVELOPMENT = True


class DevConfig(Config):
    """ Development settings class, inherits from Config. """
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    """ Testing settings class, inherits from Config."""
    TESTING = True
    HASH_ROUNDS = 1
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
