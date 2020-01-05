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

import bl
import bl.log
import bl.trm
import bl.utl

from bl.log import level
from bl.obj import Cfg, Object
from bl.trc import get_exception
from bl.trm import termsave, termreset
from bl.utl import cdir, hd

# defines

def __dir__():
    return ("HISTFILE", "close_history", "complete", "enable_history", "execute", "get_completer", "make_opts", "parse_cli", "set_completer", "writepid")

default = {
           "workdir": "",
           "kernel": False,
           "modules": "",
           "options": "",
           "prompting": True,
           "dosave": False,
           "level": "",
           "logdir": "",
           "shell": False
}

HISTFILE = ""

# functions

def close_history():
    global HISTFILE
    if bl.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bl.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            bl.utl.cdir(HISTFILE)
            bl.utl.touch(HISTFILE)
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
    if bl.obj.workdir:
        HISTFILE = os.path.abspath(os.path.join(bl.obj.workdir, "history"))
        if not os.path.exists(HISTFILE):
            touch(HISTFILE)
        else:
            readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except bl.err.EINIT:
        pass
    except PermissionError:
        pass
    except Exception:
        logging.error(get_exception())
    finally:
        termreset()

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

def parse_cli(name, version=None, opts=[], **kwargs):
    ns = Object()
    make_opts(ns, opts)
    cfg = Cfg(default)
    cfg.update(ns)
    cfg.update(kwargs)
    if "kernel" not in cfg:
        cfg.kernel = False
    if "kernel" not in cfg:
        cfg.dosave = False
    if "kernel" not in cfg:
        cfg.kernel = False
    if "kernel" not in cfg:
        cfg.kernel = False
    cfg.txt = " ".join(cfg.args)
    cfg.workdir = cfg.workdir or hd(".%s" % name)
    cfg.name = name 
    cfg.version = version or __version__
    bl.obj.workdir = cfg.workdir
    sp = os.path.join(cfg.workdir, "store") + os.sep
    if not os.path.exists(sp):
        cdir(sp)
    level(cfg.level or "error")
    logging.debug("%s started in %s at %s (%s)" % (cfg.name.upper(), cfg.workdir, time.ctime(time.time()), cfg.level))
    logging.debug(cfg)
    return cfg

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def writepid():
    assert bl.obj.workdir
    path = os.path.join(bl.obj.workdir, "pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()

# runtime

cmds = []
