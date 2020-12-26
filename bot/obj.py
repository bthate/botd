# BOTLIB - obj.py
#
# this file is placed in the public domain

"object class and methods (obj)"

# imports

import datetime
import importlib
import json
import os
import random
import sys
import time
import types
import uuid

from bot.utl import cdir, get_cls

# exceptions

class ENOFILENAME(Exception):

    "is not a filename"

# classes

class O:

    "object"

    __slots__ = ("__dict__",)

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.__dict__.update(args[0])

    def __call__(self):
        pass

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        return self.__dict__.get(k, d)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return json.dumps(self, default=default, sort_keys=True)

class Object(O):

    "id/type"

    __slots__ = ("__id__", "__type__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id__ = str(uuid.uuid4())
        self.__type__ = get_type(self)

class Default(Object):

    "default values"

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            return super().__getitem__(k, "")

class Cfg(Default):

    "config class"

class Ol(Object):

    "object list"

    def append(self, key, value):
        "add to list at self[key]"
        if key not in self:
            self[key] = []
        if isinstance(value, type(list)):
            self[key].extend(value)
        else:
            if value not in self[key]:
                self[key].append(value)

    def update(self, d):
        "to object list"
        for k, v in d.items():
            self.append(k, v)

# functions

def hook(fn):
    "construct object from filename"
    if fn.count(os.sep) > 3:
        oname = fn.split(os.sep)[-4:]
    else:
        oname = fn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    cls = get_cls(cname)
    o = cls()
    load(o, fn)
    return o

def hooked(d):
    "construct from stamp"
    from bot.obj import Object
    return Object(d)

# methods

def default(o):
    "stringified version"
    from bot.obj import Object
    if isinstance(o, Object):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
        return o
    return repr(o)

def edit(o, setter, skip=False):
    "update o from a setter dict"
    try:
        setter = vars(setter)
    except (TypeError, ValueError):
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        if skip and value == "":
            continue
        count += 1
        if value in ["True", "true"]:
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
    return count

def format(o, keys=None, skip=None):
    "1 line output string"
    if keys is None:
        keys = vars(o).keys()
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in keys:
        if key in skip:
            continue
        try:
            val = o[key]
        except KeyError:
            continue
        if not val:
            continue
        val = str(val).strip()
        res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()

def get(o, k, d=None):
    "o[k] if key, otherwise return d"
    try:
        res = o.get(k, d)
    except (TypeError, AttributeError):
        res = o.__dict__.get(k, d)
    return res

def get_name(o):
    "fully qualified name"
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

def get_type(o):
    "type"
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def items(o):
    "items (k,v)"
    try:
        return o.items()
    except (TypeError, AttributeError):
        return o.__dict__.items()

def keys(o):
    "keys"
    try:
        return o.keys()
    except (TypeError, AttributeError):
        return o.__dict__.keys()

def load(o, path):
    "from disk"
    assert path
    if path.count(os.sep) != 3:
        raise ENOFILENAME(path)
    spl = path.split(os.sep)
    stp = os.sep.join(spl[-4:])
    lpath = os.path.join(wd, "store", stp)
    typ = spl[0]
    id = spl[1]
    with open(lpath, "r") as ofile:
        try:
            v = json.load(ofile, object_hook=hooked)
        except json.decoder.JSONDecodeError as ex:
            return
        if v:
            update(o, v)
    o.__id__ = id
    o.__type__ = typ
    return stp

def mkstamp(o):
    "type/uuid/time stamp"
    timestamp = str(datetime.datetime.now()).split()
    return os.path.join(get_type(o), str(uuid.uuid4()), os.sep.join(timestamp))

def ojson(o, *args, **kwargs):
    "jsonified string"
    return json.dumps(o, default=default, *args, **kwargs)

def register(o, k, v):
    "key/value"
    o[k] = v

def save(o, stime=None):
    "to disk"
    assert wd
    if stime:
        stp = os.path.join(o.__type__, o.__id__,
                           stime + "." + str(random.randint(0, 100000)))
    else:
        timestamp = str(datetime.datetime.now()).split()
        stp = os.path.join(o.__type__, o.__id__, os.sep.join(timestamp))
    opath = os.path.join(wd, "store", stp)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(o, ofile, default=default)
    os.chmod(opath, 0o444)
    return stp

def scan(o, txt):
    "values for txt"
    for _k, v in items(o):
        if txt in str(v):
            return True
    return False

def set(o, k, v):
    "o[k]=v"
    setattr(o, k, v)

def search(o, s):
    "key,value to match dict"
    ok = False
    for k, v in items(s):
        vv = get(o, k)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def update(o, d):
    "other object"
    try:
        return o.__dict__.update(vars(d))
    except TypeError:
        return o.__dict__.update(d)

def values(o):
    "values"
    try:
        return o.values()
    except (TypeError, AttributeError):
        return o.__dict__.values()

def xdir(o, skip=None):
    "dir(o) with keys skipped"
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res

# runtime

#: working directory
wd = ""
 