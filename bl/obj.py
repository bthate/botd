# BOTD - python3 IRC channel daemon.
#
# big O Object.

import bl
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
    return ("ObjectDecoder", "ObjectEncoder", "Object", "Default", "Cfg", "Register", "edit", "eq", "format", "hooked", "items", "keys", "ne", "search", "setter", "sliced", "stamp", "update2", "values", "xdir")

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
        path = os.path.join(get_type(self), stime)
        self._path = path
        if args:
            self.update(args[0])
        if kwargs:
            self.update(kwargs)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def get(self, k, d=None):
        try:
            return self.__dict__.__getitem__(k)
        except:
            return d

    def json(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def last(self):
        from bl.dbs import Db
        db = Db()
        return db.last(str(get_type(self)))

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

    def set(self, k, v):
        self.__dict__[k] = v

    def update(self, o, skip=False):
        try:
            oo = vars(o)
        except TypeError:
            oo = o
        self.__dict__.update(oo)

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]

class Cfg(Default):

    pass


class Register(Object):

    def register(self, k, v):
        self.set(k, v)

# funcions

def edit(o, setter):
    if not setter:
        setter = {}
    count = 0
    for key, value in items(setter):
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

def eq(o1, o2):
    if isinstance(o2, (Dict, dict)):
        return o1.__dict__ == o2.__dict__
    return False

def format(o, keys=None, full=False):
    if keys is None:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if "ignore" in dir(o) and key in o.ignore:
            continue
        val = o.get(key, None)
        if not val:
            continue
        val = str(val)
        if key == "text":
            val = val.replace("\\n", "\n")
        if full:
            res.append("%s=%s " % (key, val))
        else:
            res.append(val)
    for val in res:
         txt += "%s%s" % (val.strip(), " ")
    return txt.strip()

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
    else:
        o = Object()
    o.update(d)
    return o

def items(o):
    try:
       return o.__dict__.items()
    except AttributeError:
       return o.items()
 
def keys(o):
    return o.__dict__.keys()

def ne(o1, o2):
    return o1.__dict__ != o2.__dict__

def search(o, match={}):
    res = False
    for key, value in items(match):
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
            set(o, key, True)
        elif value in ["False", "false"]:
            set(o, key, False)
        elif otype == list:
            set(o, key, value)
        elif otype == str:
            set(o, key, value)
        else:
            setattr(o, key, value)
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
        oo = o.get(k)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o.set(k, oo)
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def update2(o1, o2):
    try:
        o1.__dict__.update(o2)
    except:
        o1.update(o2)

def values(o):
    return o.__dict__.values()

def xdir(o, skip=""):
    for k in dir(o):
        if skip and skip in k:
             continue
        yield k
