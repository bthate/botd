# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import botd.tbl

from botd.dbs import Db
from botd.krn import kernels, __version__
from botd.usr import Users

# defines

def __dir__():
    return ("cmds",)

k = kernels.get_first()

# commands

def cmds(event):
    event.reply(",".join(sorted(botd.tbl.modules)))

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
    Users().meet(origin, perms)
    event.reply("added %s" % origin)

def users(event):
    res = ""
    db = Db()
    for o in db.all("botd.usr.User"):
        res += "%s," % o.user
    event.reply(res)

# runtime

k.add("cmds", cmds)
k.add("meet", meet)
k.add("users", users)
