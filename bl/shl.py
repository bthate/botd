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
import bl.pst

from bl.err import EINIT
from bl.krn import Cfg, __version__
from bl.log import level, logfiled
from bl.obj import Default, Object
from bl.trm import reset, save
from bl.utl import cdir, hd, touch
from bl.trc import get_exception

cmds = []

HISTFILE = ""

def __dir__():
    return ("daemon", "execute", "parse_cli", "set_completer")

def close_history():
    global HISTFILE
    if bl.pst.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bl.pst.workdir, "history")
        if not os.path.isfile(HISTFILE):
            cdir(HISTFILE)
            touch(HISTFILE)
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
    if bl.pst.workdir:
        HISTFILE = os.path.abspath(os.path.join(bl.pst.workdir, "history"))
        if not os.path.exists(HISTFILE):
            touch(HISTFILE)
        else:
            readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    save()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except EINIT:
        pass
    except PermissionError:
        pass
    except Exception:
        logging.error(get_exception())
    reset()
    close_history()

def get_completer():
    return readline.get_completer()

def make_opts(ns, options, **kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    for opt in options:
        if not opt:
            continue
        if opt[2] == "store":
            parser.add_argument(opt[0], opt[1], action=opt[2], type=opt[3], help=opt[4], dest=opt[5])
        else:
            parser.add_argument(opt[0], opt[1], action=opt[2], default=opt[3], help=opt[4], dest=opt[5])
    parser.add_argument('args', nargs='*')
    parser.parse_known_args(namespace=ns)

def parse_cli(name, version=None, opts=[]):
    ns = Object()
    make_opts(ns, opts)
    cfg = Cfg(ns)
    cfg.changed = not (not cfg)
    cfg.txt = " ".join(cfg.args)
    cfg.workdir = cfg.workdir or hd(".botd")
    cfg.name = name or "botd"
    cfg.version = version or __version__
    bl.pst.workdir = cfg.workdir
    sp = os.path.join(cfg.workdir, "store") + os.sep
    if not os.path.exists(sp):
        cdir(sp)
    level(cfg.level or "error")
    logging.debug("%s started in %s at %s (%s)" % (cfg.name.upper(), cfg.workdir, time.ctime(time.time()), cfg.level))
    return cfg

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def writepid():
    assert bl.pst.workdir
    path = os.path.join(bl.pst.workdir, "botlib.pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
