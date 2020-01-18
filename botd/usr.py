# BOTD - IRC channel daemon.
#
# user management.

""" user management. """

import logging

from botd.dbs import Db
from botd.obj import Object

# defines

def __dir__():
    return ("User", "Users", "meet", "users")

# classes

class User(Object):

    """
        user class.
        
        contains data for a single user.
        
    """

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Db):

    """
        users class.
        
        database object to manage users.
        
    """

    cache = Object()
    userhosts = Object()

    def allowed(self, origin, perm):
        """
            allowed method.
            
            check whether a user ia allowed to give commands.

        """
        perm = perm.upper()
        origin = self.userhosts.get(origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        logging.error("denied %s" % origin)
        return False

    def delete(self, origin, perm):
        """
            delete method.
            
            delete a permission.
            
        """
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        """
            get_users method.
            
            return all users matching the origin.
            
        """
        s = {"user": origin}
        return self.all("botd.usr.User", s)

    def get_user(self, origin):
        """
            get_user method.
            
            return last object matching origin.
            
        """
        if origin in Users.cache:
            return Users.cache[origin]
        u =  list(self.get_users(origin))
        if u:
            Users.cache[origin] = u[-1]
            return u[-1]
 
    def meet(self, origin, perms=None):
        """
            meet method.
            
            add a user to the database.
            
        """
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        user.save()
        return user

    def oper(self, origin):
        """
           oper method
           
           create a temp. users with oper permissions (doesn't save).
           
        """
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        Users.cache[origin] = user
        return user

    def perm(self, origin, permission):
        """
            perm method.
            
            add permission to a user object.
            
        """
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

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
