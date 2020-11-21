"commands (cmd)"

def __dir__():
    return ("Log", "Todo", "cmd", "dne", "fnd", "log", "todo", "thr", "ver")

import os
import sys
import threading
import time

from bot.dbs import find, list_files
from bot.hdl import mods
from bot.obj import Default, Object, cdir, fntime, get, keys, save, update
from bot.ofn import format
from bot.prs import elapsed, parse

starttime = time.time()

class Log(Object):

    "log items"

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    "todo items"

    def __init__(self):
        super().__init__()
        self.txt = ""

def cmd(event):
    "list commands (cmd)"
    c = sorted(keys(event.src.cbs))
    if c:
        event.reply(",".join(c))

def dne(event):
    "flag as done (dne)"
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("bot.cmd.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def thr(event):
    "list tasks (tsk)"
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, thr)
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def fnd(event):
    "find objects (fnd)"
    if not event.args:
        fls = event.src.files()
        if fls:
            event.reply(fls)
        return
    nr = -1
    for otype in get(event.src.names, event.args[0], [event.args[0]]):
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, event.xargs, skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)

def log(event):
    "log some text (log)"
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def tdo(event):
    "add a todo item (tdo)"
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")

def ver(event):
    versions = Object()
    for mod in mods("bot"):
        try:
            versions[mod.__name__.upper()] = mod.__version__
        except:
            pass
    if versions:
        event.reply(format(versions))
