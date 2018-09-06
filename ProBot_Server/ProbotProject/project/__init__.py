# project/__init__.py


#################
#### imports ####
#################

import os
import ConfigParser as configparser

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from project.saferproxyfix import SaferProxyFix

################
#### config ####
################

basedir = os.path.abspath(os.path.dirname(__file__))

#  env variables ./project/config/env.cfg
config_path = os.path.join(basedir, 'config', 'env.cfg')

# if config file exists, read it:
if os.path.isfile(config_path):
    config = configparser.ConfigParser()

    with open(config_path) as configfile:
        config.readfp(configfile)


def _check_config_variables_are_set(config):
    assert config['MAIL_USERNAME'] is not None,\
           'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME.'

    assert config['MAIL_PASSWORD'] is not None,\
           'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD '\

    assert config['SECRET_KEY'] is not None,\
           'SECRET_KEY is not set.'

    assert config['SECURITY_PASSWORD_SALT'] is not None,\
           'SECURITY_PASSWORD_SALT is not set.'
           
    assert config['SQLALCHEMY_DATABASE_URI'] is not None,\
           'SQLALCHEMY_DATABASE_URI is not set.'

    if config.get('environment', 'APP_SETTINGS') == 'project.config.ProductionConfig':
        assert config['STRIPE_SECRET_KEY'] is not None,\
               'STRIPE_SECRET_KEY is not set.'
        assert config['STRIPE_PUBLISHABLE_KEY'] is not None,\
               'STRIPE_PUBLISHABLE_KEY is not set.'


app = Flask(__name__)

app.config.from_object(config.get('environment', 'APP_SETTINGS'))
_check_config_variables_are_set(app.config)


##########################
#### flask-SQLAlchemy ####
##########################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#####################
#### flask-mqtt ####
#####################


####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)


app.wsgi_app = SaferProxyFix(app.wsgi_app)

####################
#### blueprints ####
####################

from project.user.views import user_blueprint, main_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)

#####################
#### flask-login ####
#####################

from project.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


########################
#### error handlers ####
########################


@app.errorhandler(Exception)
def exception_handler(error):
    return render_template("errors/error.html", modal = 'errorModal')
 
