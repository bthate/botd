# BOTD - IRC channel daemon.
#
# user management.

""" user management. """

import logging

from botd.dbs import Db
from botd.usr import Users

# defines

def __dir__():
    return ("meet", "users")

# commands

def meet(event):
    """
        meet <userhost|nick>
    
        add a user to the bot, the bot is default in deny mode.
        before the bot can be used a user must be introduced to the bot with the meet command.

    """
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

def users(event):
    """
        users command
    
        show list of introduced users.

    """
    res = ""
    db = Db()
    for o in db.all("botd.usr.User"):
        res += "%s," % o.user
    event.reply(res)
