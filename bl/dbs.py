# BOTLIB - Framework to program bots.
#
# databases. 

import os
import time
import bl
import _thread

def __dir__():
    return ("Db",)

lock = _thread.allocate_lock()

class Db(bl.Persist):

    def all(self, otype, selector=None, index=None, delta=0):
        if not selector:
            selector = {}
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not bl.obj.search(o, selector):
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
            if selector and not bl.obj.search(o, selector):
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
            if bl.obj.search(o, selector):
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
            if selector and bl.obj.search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                res.append((fn, o))
            else:
                res.append((fn, o))
        if res:
            s = sorted(res, key=lambda x: bl.tms.fntime(x[0]))
            if s:
                return s[-1][-1]
        return None

@bl.locked(lock)
def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        raise bl.err.ENOFILE(fn)
    o = bl.typ.get_cls(t)()
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
                if bl.tms.fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=bl.tms.fntime)
