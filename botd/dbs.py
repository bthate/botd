# BOTD - python3 IRC channel daemon.
#
# databases. 

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

    def all(self, otype, selector={}, index=None, delta=0):
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            yield o

    def deleted(self, otype, selector={}):
        nr = -1
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if selector and not o.search(selector):
                continue
            if "_deleted" not in o or not o._deleted:
                continue
            yield o

    def find(self, otype, selector={}, index=None, delta=0):
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if o.search(selector):
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

    def last_all(self, otype, selector={}, index=None, delta=0):
        res = []
        nr = -1
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
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def names(name, delta=None):
    assert botd.obj.workdir
    if not name:
        return []
    p = os.path.join(botd.obj.workdir, "store", name) + os.sep
    res = []
    now = time.time()
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(botd.obj.workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)
