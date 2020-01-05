# BOTD - python3 IRC channel daemon.
#
# edit configuration. 

from bl.dbs import Db
from bl.krn import kernels
from bl.typ import get_cls

# defines

def __dir__():
    return ("cfg",)

# functions

def cfg(event):
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
        save(l)
        event.reply("created a %s file" % cn)
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    edit(l, setter)
    save(l)
    event.reply("ok")

# runtime

k = kernels.get("0", None)
