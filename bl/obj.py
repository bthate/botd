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
    return ("ObjectDecoder", "ObjectEncoder", "Object", "Default", "Cfg", "Register", "hooked", "stamp")

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
            self._update(args[0])
        if kwargs:
            self._update(kwargs)

    def __eq__(self, o):
        if isinstance(self, (Object, dict)):
            return self.__dict__ == o.__dict__
        return False

    def __ne__(self, o):
        return self.__dict__ != o.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __setattr__(self, k, v):
        vv = self._get(k, None)
        if vv and type(vv) in [types.MethodType, types.FunctionType]:
            raise EOVERLOAD(k)
        super().__setattr__(k, v)

    def __str__(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def _display(self, o, txt=""):
        txt = txt[:]
        txt += " " + "%s %s" % (self._format(o), days(o._path))
        txt = txt.strip()
        self.reply(txt)

    def _edit(self, setter):
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
                self._set(key, True)
            elif value in ["False", "false"]:
                self._set(key, False)
            else:
                self._set(key, value)
        return count

    def _format(self, keys=None):
        if keys is None:
            keys = vars(self).keys()
        res = []
        txt = ""
        for key in keys:
            if key == "stamp":
                continue
            val = self._get(key, None)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append(val)
        for val in res:
            txt += "%s%s" % (val.strip(), " ")
        return txt.strip()

    def _get(self, k, d=None):
        try:
            return self.__dict__.__getitem__(k)
        except:
            return d

    def _items(self, o):
        try:
            return o.__dict__.items()
        except AttributeError:
           return o.items()
 
    def _keys(self, o):
        return o.__dict__.keys()

    def _json(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def _last(self):
        from bl.dbs import Db
        db = Db()
        return db._last(str(get_type(self)))

    @locked(lock)
    def _load(self, path):
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
            self._update(val)
        return self

    @locked(lock)
    def _save(self, stime=None):
        assert workdir
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        logging.debug("save %s" % self._path)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
        return self._path

    def _set(self, k, v):
        self.__dict__[k] = v

    def _search(self, match=None):
        res = False
        if not match:
            return res
        for key, value in match.items():
            val = self._get(key, None)
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

    def _setter(self, d):
        if not d:
            d = {}
        count = 0
        for key, value in d.items():
            if "," in value:
                value = value.split(",")
            otype = type(value)
            if value in ["True", "true"]:
                self._set(key, True)
            elif value in ["False", "false"]:
                self._set(key, False)
            elif otype == list:
                self._set(key, value)
            elif otype == str:
                self._set(key, value)
            else:
                self._set(key, value)
            count += 1
        return count

    def _sliced(self, keys=None):
        t = type(self)
        val = t()
        if not keys:
            keys = self._keys()
        for key in keys:
            try:
                val._set(key, self._get(key))
            except KeyError:
                pass
        return val

    def _update(self, o, skip=False):
        try:
            oo = vars(o)
        except TypeError:
            oo = o
        self.__dict__.update(oo)

    def _values(self):
        return self.__dict__.values()

    def _xdir(self, skip=""):
        for k in dir(self):
            if skip and skip in k:
                continue
            yield k

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]

class Cfg(Default):

    pass

class Register(Object):

    def _register(self, k, v):
        if k not in self:
            self._set(k, v)

# funcions

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
    else:
        o = Object()
    o._update(d)
    return o

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
