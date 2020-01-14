# BOTD - python3 IRC channel daemon
#
#

from botd.dbs import Db
from botd.krn import kernels
from botd.usr import Users

# define

k = kernels.get_first()

# functions

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

def u(event):
    res = ""
    db = Db()
    for o in db.all("botd.usr.User"):
        res += "%s," % o.user
    event.reply(res)

# runtime

k.add("meet", meet)
k.add("u", u)
