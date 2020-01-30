# BOTD - IRC channel daemon.
#
# basic commands. 

"""
    basic commands.

    provides the cmds commands to show a list of commands and
    the meet and users commands to manage users

"""

from botd.krn import kernels

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
    event.reply(",".join(sorted(k.cmds)))
