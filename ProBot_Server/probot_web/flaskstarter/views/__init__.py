from .. import app
from ..views.auth import auth
from ..views.main import main

app.register_blueprint(auth)
app.register_blueprint(main)
