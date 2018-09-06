# manage.py

import os
import datetime

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from project import app, db
from project.models import User

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        from gevent.pywsgi import WSGIServer
        from gevent.pool import Pool
        pool_size = 8
        worker_pool = Pool(pool_size)
        http_server = WSGIServer(('0.0.0.0', 5000), app, spawn=worker_pool)
        http_server.serve_forever()
    except KeyboardInterrupt:
        print "Server Stopped"
