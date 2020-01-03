# BOTD - python3 IRC channel daemon.
#
# basic commands. 

__version__ = 1

from bl.dbs import Db
from bl.krn import kernels

def __dir__():
    return ("cfg",)

k = kernels.get("0")

def cfg(event):
    if "IRC" in event.orig:
        event.reply("this command might flood, use a DCC connection.")
        return
    if not event.args:
        event.reply(str(k.cfg))
        return
    cn = "botd.%s.Cfg" % event.args[0]
    db = Db()
    l = db.last(cn)
    if not l:     
        try:
            cls = get_cls(cn)
        except (AttributeError, ModuleNotFoundError):
            event.reply("no %s found." % cn)
            return
        l = cls()
        l.save()
        event.reply("created a %s file" % cn)
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    edit(l, setter)
    l.save()
    event.reply("ok")

