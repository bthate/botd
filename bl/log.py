# BOTLIB - Framework to program bots.
#
# logging.

import bl
import logging
import logging.handlers
import os

from bl.pst import workdir
from bl.utl import cdir, touch

logfiled = ""

class DumpHandler(logging.StreamHandler):

    propagate = False

    def emit(self, record):
        pass



def level(loglevel="", logdir="", logfile="", nostream=False):
    global logfiled
    if not loglevel:
        loglevel = "error"
    if not logfile:
        logfile = "botd.log"
    logdir = logdir or os.path.join(workdir, "logs")
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
            logging.warn("worng level %s" % loglevel)
            loglevel = "error"
    formatter2 = logging.Formatter(format_time, datefmt)
    filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
    filehandler.propagate = False
    filehandler.setFormatter(formatter2)
    filehandler.setLevel(loglevel)
    logger.addHandler(filehandler)
    return logger
