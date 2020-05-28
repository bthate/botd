# BOTLIB - Framework to program bots.
#
#

""" framework to program bots. """

__version__ = 82

import lo
import time

from lo import get_kernel

def __dir__():
    return ("dft", "ent", "flt", "irc", "rss", "udp",  "usr", "starttime", "kernels")

#:
starttime = time.time()

