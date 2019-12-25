# BOTLIB - Framework to program bots.
#
# persistence.

import bl.krn
import datetime
import json
import json.decoder
import os
import _thread

from bl.obj import Object
from bl.typ import get_cls, get_type
from bl.utl import cdir, locked

lock = _thread.allocate_lock()

class Persist(Object):

    @locked(lock)
    def load(self, path):
        assert path
        assert bl.krn.workdir
        lpath = os.path.join(bl.krn.workdir, "store", path)
        if not os.path.exists(lpath):
            cdir(lpath)
        with open(lpath, "r") as ofile:
            try:
                val = json.load(ofile, object_hook=hooked)
            except json.decoder.JSONDecodeError as ex:
                raise bl.err.EJSON(str(ex) + " " + lpath)
            self.update(val)
        self.__path__ = path
        return self

    @locked(lock)
    def save(self, path="", stime=None):
        assert bl.krn.workdir
        self._type = get_type(self)
        if not path:
            try:
                path = self.__path__
            except AttributeError:
                pass
        if not path or stime:
            if not stime:
                stime = str(datetime.datetime.now()).replace(" ", os.sep)
            path = os.path.join(self._type, stime)
        opath = os.path.join(bl.krn.workdir, "store", path)
        bl.utl.cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(self, ofile, default=bl.obj.default, indent=4, sort_keys=True)
        self.__path__ = path
        return path

class Default(Persist):

    def __getattr__(self, k):
        if not k in self:
            self.set(k, "")
        return self.get(k)

class Cfg(Default):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            self.update(cfg)

class Register(Persist):

    def register(self, k, v):
        self.set(k, v)

def hooked(d):
    if "_type" in d:
        t = d["_type"]
        o = get_cls(t)()
    else:
        o = Object()
    o.update(d)
    return o
