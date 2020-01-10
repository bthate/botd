# BOTD - python3 IRC channel daemon.
#
# edit configuration. 

import os
import botd.obj

from botd.dbs import Db
from botd.dft import defaults
from botd.krn import kernels
from botd.typ import get_cls

# defines

def __dir__():
    return ("cfg",)

# functions

def cfg(event):
    assert(botd.obj.workdir)
    if not event.args:
        files = ["none", ] + [x.split(".")[-2].lower() for x in os.listdir(os.path.join(botd.obj.workdir, "store")) if x.endswith("Cfg")]
        if files:
            event.reply("choose from %s" % "|".join(files))
            return
        else:
            event.reply("no config files available yet.")
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
        l = cls()
        d = defaults.get(target, None)
        if d:
            l.update(d)
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
