#  logging
import logging
import socket
from .. import app
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True

f = ContextFilter()
logger = logging.getLogger()
loglevel = logging.INFO
logger.setLevel(loglevel)
logger.addFilter(f)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
host, port = app.config['LOGGING_URL'].split(':')
syslog = SysLogHandler(address=(host, int(port)))
syslog.setFormatter(formatter)
logger.addHandler(syslog)
