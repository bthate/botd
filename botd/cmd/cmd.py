# BOTD - IRC channel daemon.
#
# basic commands. 

from botd.krn import kernels

def __dir__():
    return ("cmds",)

k = kernels.get_first()

def cmds(event):
    event.reply(",".join(sorted(k.cmds)))
