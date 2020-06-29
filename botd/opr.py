# BOTLIB - the bot library !
#
#

import threading, sys, time

from bot.obj import Object, starttime
from bot.krn import k
from bot.tms import elapsed

def cfg(event):
    c = Cfg()
    last(c)
    if event.sets:
        c.update(event.sets)
        save(c)
    event.reply(format(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

def ed(event):
    if not event.args:
        event.reply(list_files(bot.obj.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = find_shorts("bot")
    if shorts:
        cn = shorts[0]
    db = Db()
    l = db.last(cn)
    if not l:
        try:
            c = get_cls(cn)
            l = c()
            event.reply("created %s" % cn)
        except ENOCLASS:
            event.reply(list_files(bot.obj.workdir) or "no files yet")
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        setter = {event.args[1]: ""}
    else:
        setter = {event.args[1]: event.args[2]}
    edit(l, setter)
    save(l)
    event.reply("ok")

def meet(event):
    if not event.args:
        event.reply("meet <userhost>")
        return
    origin = event.args[0]
    origin = k.users.userhosts.get(origin, origin)
    k.users.meet(origin)
    event.reply("ok")

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Object()
        o.update(d)
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res:
            event.reply(res.rstrip())
