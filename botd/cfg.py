# BOTLIB - Framework to program bots.
#
# edit configuration. 

from botd.dbs import Db
from botd.dft import defaults
from botd.krn import kernels
from botd.typ import get_cls

# defines

def __dir__():
    return ("cfg",)

# functions

def cfg(event):
    if not event.args:
        event.reply(str(k.cfg))
        return
    target = event.args[0]
    cn = "botd.%s.Cfg" % target
    db = Db()
    l = db.last(cn)
    if not l:     
        try:
            cls = get_cls(cn)
        except (AttributeError, ModuleNotFoundError):
            event.reply("no %s found." % cn)
            return
        d = defaults.get(target, None)
        if d:
            l = cls(d)
        else:
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
    l.edit(setter)
    l.save()
    event.reply("ok")

# runtime

k = kernels.get(0)
