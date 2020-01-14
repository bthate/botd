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

k = kernels.get_first()

# functions

def cmds(event):
    k = kernels.get_first()
    event.reply(",".join(sorted(k.cmds)))

def v(event):
    event.reply("BOTD %s" % __version__)

# runtime

k.add("cmds", cmds)
k.add("v", v)
