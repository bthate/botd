# BOTD - IRC channel daemon.
#
# kernel for boot proces.

"""
    kernel module
    
    place where commands are registered and event can get pushed to for processing.
    
"""

__version__ = 4

import inspect
import logging
import os
import time
import botd.tbl

from botd.err import EINIT
from botd.flt import Fleet
from botd.hdl import Handler
from botd.obj import Cfg, Default, Object
from botd.shl import enable_history, set_completer, writepid
from botd.trc import get_exception
from botd.usr import Users
from botd.utl import get_name

# defines

def __dir__():
    return ("Cfg", "Kernel", "Kernels", "kernels")

starttime = time.time()

# classes

class Cfg(Cfg):

    pass

class Kernel(Handler):

    """
        kernel class

        class to hold basic objects like fleet, users, runtime stash and commands.
        
    """
          
    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self.cfg = Cfg({"autoload": True, "verbose": False})
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        self.cmds = Object()
        self.fleet = Fleet()
        self.run = Default()
        self.users = Users()
        kernels.add(self)
        self.register("command", dispatch)

    def add(self, cmd, func):
        """
            add method
            
            add a command to the kernel.
            
        """
        self.cmds[cmd] = func

    def find_cmds(self, mod):
        """
            find command function.
            
            locate and register command found in a module.
            
        """
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key not in self.cmds:
                        self.add(key, o)

    def get_cmd(self, cn):
        """
            get_cmd method
            
            return a command, use autoload if not in the kernels table.
            
        """
        cmd = self.cmds.get(cn, None)
        if not cmd and self.cfg.autoload:
            mn = botd.tbl.modules.get(cn, None)
            if mn:
                self.load_mod(mn)
            cmd = self.cmds.get(cn, None)
        return cmd
 
    def load_mod(self, mn, force=False, cmds=True):
        """
            load_mod method.
            
            load a module into the kernel table and scan for commands.

        """
        mod = super().load_mod(mn, force)
        if cmds:
             self.find_cmds(mod)
        return mod
       
    def say(self, channel, txt, mtype="normal"):
        """
            say method.
            
            raw display on terminal
            
        """
        print(txt)

    def wait(self):
        """
            wait method
            
            run a loop to keep the kernel running.
            
        """
        while not self._stopped:
            time.sleep(1.0)
        logging.warn("exit")

    def walk(self, mns, init=False, cmds=True):
        """
            walk method
            
            walk over the modules in a package (or load the module directly)
            modules can have a init() function to start bots or do basic intialisation.
            you can enable this by providing init=True. use cmds=True to have the module
            scanned for commands (functions with an event parameter).

        """
        if not mns:
            return
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            m = self.load_mod(mn, False, cmds)
            if not m:
                continue
            loc = None
            if "__spec__" in dir(m):
                loc = m.__spec__.submodule_search_locations
            if not loc:
                mods.append(m)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.load_mod(mmn, False, cmds)
                        if m:
                            mods.append(m)
        if init:
            for mod in mods:
                if "init" in dir(mod):
                    mod.init(self)
        return mods


class Kernels(Object):

    """
        kernels class
        
        list of kernels. created kernels register themselves with this object.
        purpose of it is to have runtime references to kernels and not store them in the library itself.
        
    """

    kernels = []
    nr = 0

    def add(self, kernel):
        """
            add method
            
            add a kernel to the list of kernels.
            
        """
        logging.warning("add %s" % get_name(kernel))
        if kernel not in Kernels.kernels:
            Kernels.kernels.append(kernel)
            Kernels.nr += 1

    def get_first(self):
        """
            get_first method
            
            return first registered bot.
            
        """
        try:
            return Kernels.kernels[0]
        except IndexError:
            pass

# functions

def dispatch(handler, event):
    """
        dispatch handler.
        
        parse the event and dispatch to a command.
        
    """
    if not event.txt:
        return
    event.parse()
    if "_func" not in event:
        chk = event.txt.split()[0]
        event._func = handler.get_cmd(chk)
    if event._func:
        event._func(event)
        event.show()
    event.ready()

# runtime

kernels = Kernels()
