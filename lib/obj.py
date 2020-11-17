"object base class (obj)"

import datetime
import importlib
import json
import os
import random
import sys
import time
import types
import uuid
import _thread

wd = ""

class ENOFILENAME(Exception):

    "provided argument is not a filename"

class O:

    "basic object"

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

    __slots__ = ("__id__", "__type__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id__ = str(uuid.uuid4())        
        self.__type__ = get_type(self)

class Default(Object):

    "uses default values"

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            return super().__getitem__(k, "")

class Cfg(Default):

    "base config class"

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
        "update from other object list"
        for k, v in d.items():
            self.append(k, v)

# utilities

def cdir(path):
    "create directory"
    if os.path.exists(path):
        return
    res = ""
    path2, _fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
            os.chmod(padje, 0o700)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass

def fntime(daystr):
    "return time from filename"
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    try:
        datestr, rest = datestr.rsplit(".", 1)
    except ValueError:
        rest = ""
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            t += float("." + rest)
    except ValueError:
        t = 0
    return t

def get_cls(name):
    "return class from full qualified name"
    try:
        modname, clsname = name.rsplit(".", 1)
    except:
        raise ENOCLASS(name)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

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
    "construct object from stamp"
    return Object(d)

# object functions

def default(o):
    "return strinfified version of an object"
    if isinstance(o, Object):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
        return o
    return repr(o)

def get_name(o):
    "return fully qualified name of an object"
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
    "return type of an object"
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def get(o, k, d=None):
    "return o[k]"
    try:
        res = o.get(k, d)
    except (TypeError, AttributeError):
        res = o.__dict__.get(k, d)
    return res

def items(o):
    "return items (k,v) of an object"
    try:
        return o.items()
    except (TypeError, AttributeError):
        return o.__dict__.items()

def keys(o):
    "return keys of an object"
    try:
        return o.keys()
    except (TypeError, AttributeError):
        return o.__dict__.keys()

def load(o, path):
    "load from disk into an object"
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
            print(path, ex)
            return
        if v:
            update(o, v)
    o.__id__ = id
    o.__type__ = typ
    return stp
    
def register(o, k, v):
    "register key/value"
    o[k] = v

def save(o, stime=None):
    "save object to disk"
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

def set(o, k, v):
    "set o[k]=v"
    setattr(o, k, v)

def spl(txt):
    "return comma splitted values"
    return iter([x for x in txt.split(",") if x])

def update(o, d):
    "update object with other object"
    return o.__dict__.update(vars(d))

def values(o):
    "return values of an object"
    try:
        return o.values()
    except (TypeError, AttributeError):
        return o.__dict__.values()
