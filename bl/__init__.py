# BOTD - python3 IRC channel daemon.
#
# big O Object.

import bl
import datetime
import json
import logging
import os
import time
import _thread

from bl.err import EJSON
from bl.typ import get_cls, get_type
from bl.utl import cdir, locked

lock = _thread.allocate_lock()
starttime = time.time()
workdir = ""

class Object:

    __slots__ = ("__dict__", "__path__", "_type")

    def __init__(self):
        super().__init__()
        self._type = get_type(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __bool__(self):
        for k in self:
            if self.get(k, None):
                return True
        return False

    def __str__(self):
        return json.dumps(self, default=default, indent=4, sort_keys=True)

    def get(self, key, default=None):
        try:
            return self[key]
        except (TypeError, KeyError):
            try:
                return self.__dict__[key]
            except (AttributeError, KeyError):
                return getattr(self, key, default)

    def json(self):
        return json.dumps(self, default=default, sort_keys=True)

    def last(o, skip=True):
        from bl.dbs import Db
        db = Db()
        val = db.last(str(get_type(o)))
        if val:
            o.update(val)
            o.__path__ = val.__path__
            return o.__path__

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
                raise EJSON(str(ex) + " " + lpath)
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

    def set(self, key, val):
        setattr(self, key, val)

    def update(self, o, keys=None, skip=False):
        for key in o:
            val = o.get(key)
            if keys and key not in keys:
                continue
            if skip and not val:
               continue
            self.set(key, val)

class Default(Object):

    def __getattr__(self, k):
        if k in self:
            return self.__dict_[k]
        self.__dict__[k] = ""
        return self.__dict__[k]

class Cfg(Default):

    def __init__(self, cfg={}, **kwargs):
        super().__init__()
        self.update(cfg)
        self.update(kwargs)

class Register(Object):

    def register(self, k, v):
        self.set(k, v)

def default(o):
    if isinstance(o, Object):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if type(o) in [str, True, False, int, float]:
        return o
    return repr(o)

def hooked(d):
    if "_type" in d:
        t = d["_type"]
        o = get_cls(t)()
    else:
        o = Object()
    o.update(d)
    return o
