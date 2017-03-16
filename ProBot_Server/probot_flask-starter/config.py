import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    TESTING = False
    CSRF_ENABLED = True
    SECURITY_PASSWORD_SALT = 'salt-licker'

    #  SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    CONTACT_EMAIL = os.environ['CONTACT_EMAIL']

    #  gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    #  mail accounts
    MAIL_DEFAULT_SENDER = os.environ['CONTACT_EMAIL']
    #MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']

    #  flask user
    USER_ENABLE_CONFIRM_EMAIL = True

    #  remote logging
    LOGGING_URL = os.environ['LOGGING_URL']

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    ROOT_URL = 'https://robotcommander.m-iti.org'
    DATABASE = '/storage/__database.db'
    DATABASE_PATH = os.path.join(basedir, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH


class ProductionConfig(Config):
    DEBUG = False
    ROOT_URL = None


class StagingConfig(Config):
    DEBUG = False
    ROOT_URL = ''


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ROOT_URL = 'https://robotcommander.m-iti.org'
    DATABASE = 'tests.db'
    DATABASE_PATH = os.path.join(basedir, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
