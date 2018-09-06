# project/config.py

import os
import ConfigParser as configparser

basedir = os.path.abspath(os.path.dirname(__file__))


def _get_bool_env_var(varname, default=None):

    value = os.environ.get(varname, default)

    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class DevelopmentConfig(object):
    """Development configuration."""
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    #  env variables ./project/config/env.cfg
    config_path = os.path.join(basedir, 'config', 'env.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.readfp(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

        # mail settings
        MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
        MAIL_PORT = config.getint('mail', 'MAIL_PORT')
        MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
        MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

        # mail authentication and sender
        MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
        MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')

        # MQTT settings
        MQTT_SERVER_IP = config.get('MQTT', 'MQTT_SERVER_IP')
        MQTT_PORT = config.get('MQTT', 'MQTT_PORT')
