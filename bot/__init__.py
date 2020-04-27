# BOTLIB - Framework to program bots.
#
#

""" framework to program bots. """

__version__ = 81

import bot.krn
import lo
import time

def __dir__():
    return ("dft", "ent", "flt", "fnd", "irc", "krn", "rss", "shw", "udp",  "usr")

#:
starttime = time.time()

#:
kernels = []

def get_kernel(nr=0):
    return kernels[nr]
