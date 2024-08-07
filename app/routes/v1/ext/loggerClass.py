import logging

from logging.handlers import BaseRotatingHandler, TimedRotatingFileHandler
from typing import Optional
from datetime import datetime


class ProtocolLoggers:
    def __init__(self, loglevel: Optional[str] = "info", logfile: Optional[str] = None, logger_: Optional[str] = None):
        self.loglevel = loglevel
        self.logfile = logfile
        self.loggerWork = logging.getLogger(logger_)
        self.loggerWork.setLevel(self.loglevel.upper())

    def conf_log(self):
        if self.logfile:
            handler = TimedRotatingFileHandler(self.logfile, when="midnight")
        
        handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        self.loggerWork.addHandler(handler)

    def crit(self, msg: str):
        self.loggerWork.critical(msg)
    
    def err(self, msg: str):
        self.loggerWork.error(msg)

    def warn(self, msg: str):
        self.loggerWork.warning(msg)

    def info(self, msg: str):
        self.loggerWork.info(msg)

class logfileHandlers(BaseRotatingHandler):
    def __init__(self, filename, mode="a", maxBytes=0, backupCount=0, encoding="UTF-8", delay=1):
        self.filename = filename
        self.filecount = 0
        self.maxfilecount = backupCount
        super().__init__(self._get_filename(), mode, encoding, delay)

    def _get_filename(self):
        now = datetime.now()
        return self.filename.format(date=now.strftime("%Y-%m-%d"))
    
    def shouldRollOver(self, record):
        return self.filecount > self.maxfilecount
    

    def doRollOver(self):
        self.close()
        self.filecount += 1
        self.baseFilename = self._get_filename()
        self.mode = "w"
        self.stream = self._open()