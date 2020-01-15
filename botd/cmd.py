# BOTD - python3 IRC channel daemon.
#
# basic commands. 

"""
    basic commands.

    provides the cmds commands to show a list of commands and
    the meet and users commands to manage users

"""

from botd.krn import kernels
from botd.tbl import modules

# defines

def __dir__():
    return ("cmds",)

k = kernels.get_first()

# commands

def cmds(event):
    """
        cmds command
    
        show list of commands.

    """
    res = []
    for cn, mn in modules.items():
        for mmn in k.table:
            if mmn in mn:
                res.append(cn)
    if res:
        event.reply(",".join(sorted(res)))
    else:
        event.reply("no commands.")