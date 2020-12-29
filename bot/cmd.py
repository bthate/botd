# BOTD - 24/7 channel daemon (cmd.py)
#
# this file is placed in the public domain

"commands (cmd)"

# imports

import threading
import time
import bot.obj
import bot.tbl

from bot.dbs import find, last, last_match, list_files
from bot.obj import Object, edit, format, get, get_name, keys, save, update
from bot.hdl import Bus, __version__
from bot.irc import Cfg
from bot.prs import elapsed
from bot.rss import Fetcher, Rss
from bot.utl import fntime, mods

# defines

def __dir__():
    return ("Log", "Todo", "cmd", "cfg", "dpl", "dne", "flt", "fnd", "ftc", "log", "rem", "rss", "tdo", "thr", "ver")

starttime = time.time()

# classes

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

# commands

def cmd(event):
    "list commands (cmd)"
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))

def cfg(event):
    "configure irc (cfg)"
    c = Cfg()
    last(c)
    if not event.prs.sets:
        return event.reply(format(c, skip=["username", "realname"]))
    update(c, event.prs.sets)
    save(c)
    event.reply("ok")


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

def dpl(event):
    "set keys to display (dpl)"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in last_match("bot.rss.Rss", {"rss": event.args[0]}):
        edit(o, setter)
        save(o)
        event.reply("ok")

def flt(event):
    "list of bots"
    try:
        event.reply(str(Bus.objs[event.prs.index-1]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(",".join([get_name(o) for o in Bus.objs]))

def fnd(event):
    "find objects (fnd)"
    if not event.args:
        fls = list_files(bot.obj.wd)
        if fls:
            event.reply(" | ".join([x.split(".")[-1].lower() for x in fls]))
        return
    nr = -1
    for otype in get(bot.tbl.names, event.args[0], [event.args[0]]):
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, event.xargs or keys(o), skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
            
def ftc(event):
    "run a fetch (ftc)"
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def log(event):
    "log some text (log)"
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def rem(event):
    "remove a rss feed (rem)"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in find("bot.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")

def rss(event):
    "add a rss feed (rss)"
    if not event.args:
        return
    url = event.args[0]
    res = list(find("bot.rss.Rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    save(o)
    event.reply("ok")

def tdo(event):
    "add a todo item (tdo)"
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")

def thr(event):
    "list running threads (thr)"
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

def ver(event):
    "show version (ver)"
    event.reply("BOTLIB %s" % __version__)
