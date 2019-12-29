# BOTD - python3 IRC channel daemon.
#
# persistence.

import datetime
import json
import json.decoder
import logging
import os
import _thread

from bl.obj import Default, Object, default
from bl.typ import get_cls, get_type
from bl.utl import cdir, locked

lock = _thread.allocate_lock()
workdir = ""

class Persist(Object):

    @locked(lock)
    def load(self, path):
        assert path
        assert workdir
        lpath = os.path.join(workdir, "store", path)
        if not os.path.exists(lpath):
            cdir(lpath)
        logging.debug("load %s" % path)
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
        assert workdir
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
        opath = os.path.join(workdir, "store", path)
        cdir(opath)
        logging.warning("save %s" % path)
        with open(opath, "w") as ofile:
            json.dump(self, ofile, default=default, indent=4, sort_keys=True)
        self.__path__ = path
        return path

class Cfg(Default, Persist):

    def __init__(self, cfg={}, **kwargs):
        super().__init__()
        self.update(cfg)
        self.update(kwargs)

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
