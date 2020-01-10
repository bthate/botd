# BOTD - python3 IRC channel daemon.
#
# logging.

import logging
import logging.handlers
import os

import botd.obj

from botd.utl import cdir, hd, touch

# defines

def __dir__():
    return ("DumpHandler", "level", "logfiled")
    
logfiled = ""

# 

class DumpHandler(logging.StreamHandler):

    propagate = False

    def emit(self, record):
        pass

def level(loglevel="", logdir="", logfile="botd.log", nostream=False):
    global logfiled
    if not loglevel:
        loglevel = "error"
    if not logdir:
        logdir = os.path.join(hd(".botd"), "logs")
    logfile = logfiled = os.path.join(logdir, logfile)
    if not os.path.exists(logfile):
        cdir(logfile)
        touch(logfile)
    datefmt = '%H:%M:%S'
    format_time = "%(asctime)-8s %(message)-70s"
    format_plain = "%(message)-0s"
    loglevel = loglevel.upper()
    logger = logging.getLogger("")
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    try:
        logger.setLevel(loglevel)
    except ValueError:
        pass
    formatter = logging.Formatter(format_plain, datefmt)
    if nostream:
        dhandler = DumpHandler()
        dhandler.propagate = False
        dhandler.setLevel(loglevel)
        logger.addHandler(dhandler)
    else:
        handler = logging.StreamHandler()
        handler.propagate = False
        handler.setFormatter(formatter)
        try:
            handler.setLevel(loglevel)
            logger.addHandler(handler)
        except ValueError:
            logging.warn("wrong level %s" % loglevel)
            loglevel = "ERROR"
    formatter2 = logging.Formatter(format_time, datefmt)
    filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
    filehandler.propagate = False
    filehandler.setFormatter(formatter2)
    try:
        filehandler.setLevel(loglevel)
    except ValueError:
        pass
    logger.addHandler(filehandler)
    return logger
