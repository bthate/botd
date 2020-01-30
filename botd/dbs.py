# BOTD - IRC channel daemon.
#
# databases. 

"""
    database related functionality.

    provides a Db cursor to the objects stored on disk.

    >>> import botd.obj
    >>> botd.obj.workdir = "testdata"

    >>> from botd.dbs import Db
    >>> db = Db()
        
"""

import os
import time
import _thread
import botd.obj

from botd.err import ENOFILE
from botd.obj import Object, workdir
from botd.tms import fntime
from botd.typ import get_cls
from botd.utl import locked

# defines

def __dir__():
    return ("Db", "hook", "lock", "names")

lock = _thread.allocate_lock()

# classes

class Db(Object):

    """
        Db class
        
        make queries on the JSON objects possible.

    """
    
    def all(self, otype, selector={}, index=None, delta=0):
        """
            query all objects
        
            basic query need a type (full qualified name) and a selector (dict with name/values) to match the objects.
            index (number in resultset) and delta option (time diff from now) can be provided to limit search.

            by default the all method returns all records of a certain type.

            >>> for o in db.all("botd.irc.Cfg", {"server": "localhost"}): print(o)

        """
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            res.append(o)
        return res

    def deleted(self, otype, selector={}):
        """
            deleted method
        
            show deleted records, requires a type and optional selector.

            >>> for o in db.deleted("botd.krn.Cfg"): print(o)
            
        """
        nr = -1
        res = []
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if selector and not o.search(selector):
                continue
            if "_deleted" not in o or not o._deleted:
                continue
            res.append(o)
        return res
        
    def find(self, otype, selector={}, index=None, delta=0):
        """ 
            search typed objects
        
            basic query need a type (full qualified name) and a selector (dict with name/values) to match the objects.
            index (number in resultset) and delta option (time diff from now) can be provided to limit search.

            by default the find method only returns objects that match.

            >>> for o in db.find("botd.irc.Cfg", {"server": "localhost"}): print(o)

        """
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            if o.search(selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                res.append(o)
        return res

    def find_value(self, otype, values=[], index=None, delta=0):
        """ 
            search typed objects
        
            basic query need a type (full qualified name) and a selector (dict with name/values) to match the objects.
            index (number in resultset) and delta option (time diff from now) can be provided to limit search.

            by default the find method only returns objects that match.

            >>> for o in db.find_value("botd.irc.Cfg", "localhost"): print(o)

        """
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            if o.find(values):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                res.append(o)
        return res

    def last(self, otype, index=None, delta=0):
        """
            last method.
        
            return the last saved object of a type.

            >>> o = db.last("botd.rss.Rss") 
            
        """
        fns = names(otype, delta)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_all(self, otype, selector={}, index=None, delta=0):
        """
            scan the database in reverse.

            return the objects saved last while matching the provided selector.
           
            >>> o = db.last_all("botd.rss.Rss")
             
        """
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            if selector and o.search(selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                res.append((fn, o))
            else:
                res.append((fn, o))
        if res:
            s = sorted(res, key=lambda x: fntime(x[0]))
            if s:
                return s[-1][-1]
        return None

# functions

@locked(lock)
def hook(fn):
    """
        hook function.
    
        convert a filename into a object. the objects type is taken f
        rom the filename, constructed an the loaded from disk.
      
        >>> from botd.dbs import hook
        >>> o = hook("botd.rss.Rss/01-01-2020/00:00:00")

    """
    
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def names(name, delta=None):
    """
        names function.
        
        return all matching types found in the workdir.
        
        >>> from botd.dbs import names
        >>> n = names("botd.cfg.Krn")
        
    """
    assert botd.obj.workdir
    if not name:
        return []
    p = os.path.join(botd.obj.workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if delta:
        past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(botd.obj.workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)
