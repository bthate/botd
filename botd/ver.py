# BOTD - 24/7 channel dameon
#
# this file is placed in the public domain

import bot.hdl

__version__ = 26

def ver(event):
    event.reply("BOTD #%s | BOTLIB %s" % (__version__, bot.hdl.__version__))
    