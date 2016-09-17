import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.babel import Babel
from flask.json import JSONEncoder

def import_modules():
    from . import views
    from . import models
    from . import logs

class CustomJSONEncoder(JSONEncoder):
    """
    This class adds support for lazy translation texts to Flask's JSON encoder.
    This is necessary when flashing translated texts.
    """

    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            try:
                return unicode(obj)  # python 2
            except NameError:
                return str(obj)  # python 3
        return super(CustomJSONEncoder, self).default(obj)

############
# APP INIT #
############
app = Flask(__name__)
#  load settings from Config class,
#  depending on environmental variable
app.config.from_object(os.environ['APP_SETTINGS'])
app.json_encoder = CustomJSONEncoder
db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)

# import into module namespace
import_modules()
