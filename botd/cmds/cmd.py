# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import botd.tbl

from botd.krn import kernels, __version__
from botd.usr import Users

# defines

def __dir__():
    return ("cmds",)

k = kernels.get_first()

# functions

def cmds(event):
    event.reply(",".join(sorted(botd.tbl.modules)))

# runtime

k.add("cmds", cmds)
