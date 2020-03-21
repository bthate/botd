# LIBOBJ - library to manipulate objects.
#
#

import argparse
import atexit
import lo
import logging
import logging.handlers
import os
import readline
import sys
import time
import termios
import threading
import traceback

from lo.trc import get_exception

cmds = []
logfiled = ""
resume = {}
HISTFILE = ""

class ENOTXT(Exception):
    pass

class DumpHandler(logging.StreamHandler):

    propagate = False

    def emit(self, record):
        pass

def close_history():
    global HISTFILE
    if lo.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(lo.workdir, "history")
        if not os.path.isfile(HISTFILE):
            lo.cdir(HISTFILE)
            lo.touch(HISTFILE)
        readline.write_history_file(HISTFILE)

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def enable_history():
    global HISTFILE
    if lo.workdir:
        HISTFILE = os.path.abspath(os.path.join(lo.workdir, "history"))
        if not os.path.exists(HISTFILE):
            lo.cdir(HISTFILE)
            lo.touch(HISTFILE)
        else:
            readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    except Exception:
        logging.error(get_exception())
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

def level(loglevel, logfile, nostream=False):
    assert lo.workdir
    assert logfile
    global logfiled
    if not os.path.exists(logfile):
        lo.cdir(logfile)
        lo.touch(logfile)
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
            logging.warning("wrong level %s" % loglevel)
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

def make_opts(ns, options, usage="", **kwargs):
    kwargs["usage"] = usage
    parser = argparse.ArgumentParser(**kwargs)
    for opt in options:
        if not opt:
            continue
        if opt[2] == "store":
            parser.add_argument(opt[0], opt[1], action=opt[2], type=opt[3], default=opt[4], help=opt[5], dest=opt[6], const=opt[4], nargs="?")
        else:
            parser.add_argument(opt[0], opt[1], action=opt[2], default=opt[3], help=opt[4], dest=opt[5])
    parser.add_argument('args', nargs='*')
    parser.parse_known_args(namespace=ns)

def parse_cli(name, version=lo.__version__, opts=None, usage="", lf=None):
    ns = lo.Object()
    if opts:
        make_opts(ns, opts, usage)
    cfg = lo.Default(ns)
    cfg.name = name
    cfg.version = version
    cfg.txt = " ".join(cfg.args)
    if not cfg.workdir:
        cfg.workdir = lo.hd(".%s" % name)
    lo.workdir = cfg.workdir
    lo.cdir(os.path.join(lo.workdir, "store", ""))
    if lf or cfg.logfile:
        lo.cdir(lf or cfg.logfile)
    lo.cfg.update(cfg)
    return cfg

def rlog(level, txt, extra):
    logging.log(level, "%s %s" % (txt, extra))

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
        
def setup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass    

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def writepid():
    assert lo.workdir
    path = os.path.join(lo.workdir, "pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
