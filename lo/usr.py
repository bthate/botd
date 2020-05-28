# BOTLIB - Framework to program bots.
#
#

""" user management. """

import lo
import logging

def __dir__():
    return ("User", "Users", "meet", "users")

class User(lo.Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(lo.Db):

    userhosts = lo.Object()

    def allowed(self, origin, perm, log=True):
        k = lo.get_kernel()
        if k.cfg.owner and origin != k.cfg.owner:
             return True
        perm = perm.upper()
        origin = self.userhosts.get(origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        if log:
            logging.error("denied %s" % origin)
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return self.all("lo.usr.User", s)

    def get_user(self, origin):
        u =  list(self.get_users(origin))
        if u:
            return u[-1]
 
    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        user.save()
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

def meet(event):
    k = lo.get_kernel()
    if not event.origin == k.cfg.owner:
        event.reply("only owner can add users")
        return
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    k = lo.get_kernel()
    origin = lo.usr.Users.userhosts.get(origin, origin)
    k.users.meet(origin, perms)
    event.reply("ok")

def users(event):
    k = lo.get_kernel()
    res = ""
    db = lo.Db()
    for o in db.all("lo.usr.User"):
        res += "%s," % o.user
    event.reply(res)
