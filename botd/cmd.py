# BOTLIB - the bot library !
#
#

__version__ = 1

import os
import time

import bot.obj

from bot.dbs import Db, last
from bot.fil import cdir
from bot.irc import Cfg
from bot.krn import k, starttime
from bot.obj import Object, format, get_type, save
from bot.tms import elapsed, fntime

from botd.version import __version__

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def cfg(event):
    c = Cfg()
    last(c)
    if not event.args and not event.sets:
        event.reply(format(c))
        return
    if event.sets:
        c.update(event.sets)
        save(c)
    event.reply(format(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    db = Db()
    for o in db.find("botd.cmd.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def find(event):
    if event.speed != "fast":
        event.reply("use a faster bot to display (dcc).")
        return
    if not event.args:
        wd = os.path.join(bot.obj.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    db = Db()
    target = db.all
    otype = event.args[0]
    try:
        match = event.args[1]
        target = db.find_value
    except IndexError:
        match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for o in target(otype, match):
        nr += 1
        event.display(o, str(nr), args or o.keys())
    if nr == -1:
        event.reply("no %s found." % otype)

def fl(event):
    try:
        index = int(event.args[0])
        if event.speed != "fast":
            event.reply("use a faster bot to display.")
            return
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def log(event):
    if not event.rest:
        db = Db()
        res = db.find("botd.cmd.Log", {"txt": ""})
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("log what ?")
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def todo(event):
    db = Db()
    if not event.rest:
        res = db.find("botd.cmd.Todo", {"txt": ""})
        if not res:
            return
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("do what ?")
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("%s %s" % (k.cfg.name.upper() or "BOTLIB", k.cfg.version or __version__))
