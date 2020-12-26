# BOTLIB - usr.py
#
# this file is placed in the public domain

"users (usr)"

# imports

from bot.obj import Object, get, save
from bot.dbs import find

# exceptions

class ENOUSER(Exception):
    "no matching user found."
    
# classes

class User(Object):

    "user"

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Object):

    "users"

    userhosts = Object()

    def allowed(self, origin, perm):
        "origin has needed permission"
        perm = perm.upper()
        origin = get(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        "permission"
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        "all users, optionaly matching origin"
        s = {"user": origin}
        return find("bot.usr.User", s)

    def get_user(self, origin):
        "specific user with matching origin"
        u = list(self.get_users(origin))
        if u:
            return u[-1][-1]

    def meet(self, origin, perms=None):
        "user"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        "grant oper permission"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        "add permission"
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user
