import logging
from logging.handlers import RotatingFileHandler

log = logging.getLogger('applogger')
log.setLevel(logging.DEBUG)

logFile = "log/UC.log"
handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(format)

log.addHandler(handler)
