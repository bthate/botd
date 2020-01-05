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
    return ("ObjectDecoder", "ObjectEncoder", "Object", "Default", "Cfg", "hooked", "stamp")

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
    else:
        o = Object()
    update(o, d)
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

class Object:

    __slots__ = ("__dict__", "_path")

    def __init__(self, *args, **kwargs):
        super().__init__()
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self._path = os.path.join(get_type(self), stime)
        if args:
            update(self, args[0])
        if kwargs:
            update(self, kwargs)

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return to_json(self)

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]

class Cfg(Object):

    pass

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
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
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

def get(o, k, d=None):
    try:
        return o[k]
    except KeyError:
        return d

def items(o):
    return o.__dict__.items()

def keys(o):
    return o.__dict__.keys()

def last(o):
    from bl.dbs import Db
    db = Db()
    return db.last(str(get_type(o)))

@locked(lock)
def load(o, path):
    assert path
    assert workdir
    lpath = os.path.join(workdir, "store", path)
    if not os.path.exists(lpath):
        cdir(lpath)
    logging.debug("load %s" % path)
    o._path = path
    with open(lpath, "r") as ofile:
        try:
            val = json.load(ofile, cls=ObjectDecoder)
        except json.decoder.JSONDecodeError as ex:
            raise EJSON(str(ex) + " " + lpath)
        update(o, val)
    return o

def merge(o1, o2):
    return update(o1, strip(o2))

@locked(lock)
def save(o, stime=None):
    assert workdir
    opath = os.path.join(workdir, "store", o._path)
    cdir(opath)
    logging.debug("save %s" % o._path)
    with open(opath, "w") as ofile:
        json.dump(stamp(o), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
    return o._path

def search(o, match=None):
    res = False
    if not match:
        return res
    for key, value in match.items():
        val = get(o, key, None)
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

def set(o, k, v):
    o[k] = v

def setter(o, d):
    if not d:
        d = {}
    count = 0
    for key, value in d.items():
        if "," in value:
            value = value.split(",")
        otype = type(value)
        if value in ["True", "true"]:
            set(o, key, True)
        elif value in ["False", "false"]:
            set(o, key, False)
        elif otype == list:
            set(o, key, value)
        elif otype == str:
            set(o, key, value)
        else:
            set(o, key, value)
        count += 1
    return count

def sliced(o, keys=None):
    t = type(o)
    val = t()
    if not keys:
        keys = keys(o)
    for key in keys:
        try:
            val[key] = o[key]
        except KeyError:
            pass
    return val

def stamp(o):
    for k in dir(o):
        oo = get(o, k)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def strip(o):
    for k in o:
       if not k:
          del o[k]
    return o

def to_json(o):
    return json.dumps(o, cls=ObjectEncoder, indent=4, sort_keys=True)

def update(o1, o2, keys=None, skip=None):
    for key in o2:
        if keys and key not in keys:
            continue
        if skip and key in skip:
            continue
        set(o1, key, get(o2, key))

def values(o):
    return o.__dict__.values()

def xdir(o, skip=""):
    res = []
    for k in dir(o):
        if skip and skip in k:
            continue
        res.append(k)
    return res
