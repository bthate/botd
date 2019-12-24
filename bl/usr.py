# BOTLIB - Framework to program bots.
#
# user management.

import bl

def __dir__():
    return ("User", "Users", "meet")

class User(bl.Persist):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(bl.Persist):

    cache = bl.Object()
    userhosts = bl.Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
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
        return bl.db.all("bl.usr.User", s)

    def get_user(self, origin):
        u =  list(self.get_users())
        if u:
            return u[-1]
 
    def meet(self, origin, perms=None):
        if not perms:
            perms = []
        user = self.get_user(origin)
        if not user:
            user = User()
        user.user = origin
        user.perms = perms + ["USER", ]
        if perms:
            user.perms.extend(perms)
        user.save()
        return user

    def oper(self, origin):
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        bl.set(Users.cache, origin, user)
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise bl.err.ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user
