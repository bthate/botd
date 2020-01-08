# BOTD - python3 IRC channel daemon.
#
# basic commands. 

from botd.obj import Object
from botd.dbs import Db
from botd.krn import kernels, __version__
from botd.usr import Users

# defines

def __dir__():
    return ("cmds", "meet", "u", "v")

# functions

def cmds(event):
    k = kernels.get(0)
    event.reply(",".join(sorted(k.cmds)))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    k = kernels.get(0)
    origin = Users.userhosts.get(origin, origin)
    u = k.users.meet(origin, perms)
    event.reply("added %s" % origin)

def u(event):
    res = ""
    db = Db()
    for o in db.all("botd.usr.User"):
        res += "%s," % o.user
    event.reply(res)

def v(event):
    event.reply("BOTD %s" % __version__)
