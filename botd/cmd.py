# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import time

from bl.dbs import Db
from bl.krn import kernels, __version__
from bl.tms import elapsed
from bl.usr import Users

# defines

def __dir__():
    return ("cmds", "meet", "u", "v")

# functions

def cmds(event):
    event.reply(",".join(k.cmds))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = Users.userhosts.get(origin, origin)
    u = k.users.meet(origin, perms)
    event.reply("added %s" % origin)

def u(event):
    res = ""
    db = Db()
    for o in db.all("bl.usr.User"):
        res += "%s," % o.user
    event.reply(res)

def v(event):
    event.reply("BOTD %s" % __version__)

# runtime

k = kernels.get("0", None)
