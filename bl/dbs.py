# BOTD - python3 IRC channel daemon.
#
# databases. 

import bl
import os
import time
import _thread

from bl import Object
from bl.err import ENOFILE
from bl.gnr import search
from bl.tms import fntime
from bl.typ import get_cls
from bl.utl import locked

def __dir__():
    return ("Db",)

lock = _thread.allocate_lock()

class Db(Object):

    def all(self, otype, selector=None, index=None, delta=0):
        if not selector:
            selector = {}
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            yield o

    def deleted(self, otype, selector={}):
        if not selector:
            selector = {}
        nr = -1
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if selector and not search(o, selector):
                continue
            if "_deleted" not in o or not o._deleted:
                continue
            yield o

    def find(self, otype, selector={}, index=None, delta=0):
        if not selector:
            selector = {}
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def last(self, otype, index=None, delta=0):
        fns = names(otype, delta)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_all(self, otype, selector=None, index=None, delta=0):
        if not selector:
            selector = {}
        res = []
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if selector and search(o, selector):
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

@locked(lock)
def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def names(name, delta=None):
    assert bl.workdir
    p = os.path.join(bl.workdir, "store", name) + os.sep
    res = []
    now = time.time()
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(bl.workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

def last(o, skip=True):
    db = Db()
    val = db.last(str(str(bl.typ.get_type(o))))
    if val:
        o.update(val)
        o.__path__ = val.__path__
        return o.__path__
