# BOTD - 24/7 channel dameon
#
#

import bot.hdl

__version__ = 25

def ver(event):
    event.reply("BOTD #%s | BOTLIB %s" % (__version__, bot.hdl.__version__))
    