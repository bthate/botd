# BOTD - python3 IRC channel daemon.
#
# shell related code.

import argparse
import atexit
import logging
import optparse
import os
import readline
import time

import botd.log
import botd.trm
import botd.utl

from botd.dft import defaults
from botd.log import level, logfiled
from botd.obj import Cfg, Object
from botd.trc import get_exception
from botd.trm import termsave, termreset
from botd.utl import cdir, hd

# defines

def __dir__():
    return ("HISTFILE", "close_history", "complete", "enable_history", "get_completer", "make_opts", "parse_cli", "set_completer", "writepid")

HISTFILE = ""

opts = [
    ('-b', '--daemon', 'store_true', False, 'enable daemon mode', 'daemon'),
    ('-d', '--datadir', 'store', str, "", 'set working directory.', 'workdir'),
    ('-m', '--modules', 'store', str, "", 'modules to load.', 'modules'),
    ('-l', '--loglevel', 'store', str, "", 'set loglevel.', 'level'),
    ('-a', '--logdir', "store", str, "", "directory to find the logfiles.", 'logdir'),
]

# functions

def close_history():
    global HISTFILE
    if botd.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(botd.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            botd.utl.cdir(HISTFILE)
            botd.utl.touch(HISTFILE)
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

def enable_history():
    global HISTFILE
    if botd.obj.workdir:
        HISTFILE = os.path.abspath(os.path.join(botd.obj.workdir, "history"))
        if not os.path.exists(HISTFILE):
            touch(HISTFILE)
        else:
            readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def get_completer():
    return readline.get_completer()

def make_opts(ns, options, **kwargs):
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

def parse_cli(name, version=None, opts=opts, wd="", ld="", **kwargs):
    ns = Object()
    if opts:
        make_opts(ns, opts)
    cfg = Cfg(ns, kwargs)
    if not cfg.workdir:
        cfg.workdir = wd or hd(".botd") 
    if not cfg.logdir:
        cfg.logdir = ld or os.path.join(cfg.workdir, "logs")
    if not cfg.level:
        cfg.level = "error"
    p = os.path.join(cfg.workdir, "store")
    if not os.path.isdir(p):
        cdir(p)
    botd.obj.workdir = cfg.workdir
    cfg.name = name 
    cfg.txt = " ".join(cfg.args)
    cfg.version = version or __version__
    level(cfg.level, cfg.logdir, nostream=cfg.daemon)
    logging.warning("BOTD started at %s (%s)" % (cfg.workdir, cfg.level or "debug"))
    return cfg

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def writepid():
    assert botd.obj.workdir
    path = os.path.join(botd.obj.workdir, "pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()

# runtime

cmds = []
