# BOTD - python3 IRC channel daemon.
#
# big O Object.

import bl
import collections
import datetime
import json
import logging
import os
import time
import types
import _thread

from json import JSONEncoder, JSONDecoder

from bl.err import EJSON, EOVERLOAD
from bl.typ import get_cls, get_type
from bl.utl import cdir, locked, get_name

# defines

def __dir__():
    return ("ObjectDecoder", "ObjectEncoder", "Object", "Default", "Cfg", "Register", "hooked", "stamp")

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
    else:
        o = Object()
    o.update(d)
    return o

lock = _thread.allocate_lock()
starttime = time.time()
workdir = ""

# classes

class ObjectEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if type(o) in [str, True, False, int, float]:
            return o
        return repr(o)

class ObjectDecoder(JSONDecoder):

    def decode(self, s):
        if s == "":
            return Object()
        return json.loads(s, object_hook=hooked)

class Object(collections.MutableMapping):

    __slots__ = ("__dict__", "_path")

    def __init__(self, *args, **kwargs):
        super().__init__()
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        path = os.path.join(get_type(self), stime)
        self._path = path
        if args:
            self.update(args[0])
        if kwargs:
            self.update(kwargs)

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    @locked(lock)
    def load(self, path):
        assert path
        assert workdir
        lpath = os.path.join(workdir, "store", path)
        if not os.path.exists(lpath):
            cdir(lpath)
        logging.debug("load %s" % path)
        self._path = path
        with open(lpath, "r") as ofile:
            try:
                val = json.load(ofile, cls=ObjectDecoder)
            except json.decoder.JSONDecodeError as ex:
                raise EJSON(str(ex) + " " + lpath)
            self.update(val)
        return self

    @locked(lock)
    def save(self, stime=None):
        assert workdir
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        logging.debug("save %s" % self._path)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
        return self._path

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]

class Cfg(Object):

    pass

class Register(Object):

    def register(self, k, v):
        if k not in self:
            self[k] = v

# functions

def edit(o, setter):
    try:
        setter = vars(setter)
    except:
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        count += 1
        if "," in value:
            value = value.split(",")
        if value in ["True", "true"]:
            o.set(key, True)
        elif value in ["False", "false"]:
            o.set(key, False)
        else:
            o.set(key, value)
    return count

def format(o, keys=None):
    if keys is None:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if key == "stamp":
            continue
        val = o.get(key, None)
        if not val:
            continue
        val = str(val)
        if key == "text":
            val = val.replace("\\n", "\n")
        res.append(val)
    for val in res:
        txt += "%s%s" % (val.strip(), " ")
    return txt.strip()

def to_json(o):
    return json.dumps(o, cls=ObjectEncoder, indent=4, sort_keys=True)

def last(o):
    from bl.dbs import Db
    db = Db()
    return db.last(str(get_type(o)))

def merge(o1, o2):
    return o1.update(strip(o2))

def search(o, match=None):
    res = False
    if not match:
        return res
    for key, value in match.items():
        val = o.get(key, None)
        if val:
            if not value:
                res = True
                continue
            if value in str(val):
                res = True
                continue
            else:
                res = False
                break
        else:
            res = False
            break
    return res

def setter(o, d):
    if not d:
        d = {}
    count = 0
    for key, value in d.items():
        if "," in value:
            value = value.split(",")
        otype = type(value)
        if value in ["True", "true"]:
            o.set(key, True)
        elif value in ["False", "false"]:
            o.set(key, False)
        elif otype == list:
            o.set(key, value)
        elif otype == str:
            o.set(key, value)
        else:
            o.set(key, value)
        count += 1
    return count

def sliced(o, keys=None):
    t = type(o)
    val = t()
    if not keys:
        keys = o.keys()
    for key in keys:
        try:
            val[key] = o[key]
        except KeyError:
            pass
    return val

def stamp(o):
    for k in dir(o):
        oo = o._get(k)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o._set(k, oo)
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def strip(o):
    for k in o:
       if not k and k is not None:
          del o[k]
    return o

def xdir(o, skip=""):
    for k in dir(o):
        if skip and skip in k:
            continue
        yield k
