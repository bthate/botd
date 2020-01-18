# BOTD - python3 IRC channel daemon.
#
# big O Object.

"""
    obj module.
    
    provide a object class that can do persistence (load/save) to objects.
    use JSON to serialize objects to/from disk.
    
"""

import collections
import datetime
import json
import logging
import os
import time
import types
import _thread

from json import JSONEncoder, JSONDecoder

from botd.err import EJSON, EOVERLOAD, ETYPE
from botd.typ import get_cls, get_type
from botd.utl import cdir, locked, get_name

# defines

def __dir__():
    return ("ObjectDecoder", "ObjectEncoder", "Object", "Default", "Cfg", "hooked", "stamp")

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

    """
        objectencoder class
        
        used to serialize objects to strings.
        
    """   

    def default(self, o):
        """
            default method.
            
            return stringable representation of an object.
            
        """
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

    """
        objectdecoder class.
        
        used to reconstruct an object from JSON
        
    """

    def decode(self, s):
        """
            decode method.
            
            decode JSON string to it's corresponding object (convert to type).
            
        """
        if s == "":
            return Object()
        return json.loads(s, object_hook=hooked)

class O:

    """ 
        o class.
        
        basic object to hook persistence into.
        
    """

    __slots__ = ("__dict__", "_path")

    def __init__(self, *args, **kwargs):
        super().__init__()
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self._path = os.path.join(get_type(self), stime)

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


class Object(O, collections.MutableMapping):

    """
        object class.
        
        persistable, inheritable object.
        
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            try:
                self.update(args[0])
            except TypeError:
                self.update(vars(args[0]))
        if kwargs:
            self.update(kwargs)

    def __str__(self):
        return self.json()

    def edit(self, setter, skip=False):
        """
            edit method.
            
            update the object to a setter key/value dict.
            
        """
        try:
            setter = vars(setter)
        except:
            pass
        if not setter:
            setter = {}
        count = 0
        for key, value in setter.items():
            if skip and value == "":
                continue
            count += 1
            if value in ["True", "true"]:
                self[key] = True
            elif value in ["False", "false"]:
                self[key] = False
            else:
                self[key] = value
        return count

    def find(self, val):
        """
            find method.
            
            see if val is in one of the object's values.
            
        """
        for item in self.values():
            if val in item:
                return True
        return False

    def format(self, keys=None):
        """
            format method.
            
            format the object to a printable string, using provided keys (or all keys if none given).
            
        """
        if keys is None:
            keys = vars(self).keys()
        res = []
        txt = ""
        for key in keys:
            if key == "stamp":
                continue
            val = self.get(key, None)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append(val)
        for val in res:
            txt += "%s%s" % (val.strip(), " ")
        return txt.strip()

    def json(self):
        """
            json method.
            
            return json string of the objects.
            
        """
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def last(self, strip=False):
        """
            last method.
            
            return last saved object of this type.
            
        """
        from botd.dbs import Db
        db = Db()
        l = db.last(str(get_type(self)))
        if l:
            if strip:
                self.update(strip(l))
            else:
                self.update(l)

    @locked(lock)
    def load(self, path):
        """
            load method.
            
            load object from disk.

        """
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
            ot = val.__dict__["stamp"].split(os.sep)[0]
            t = get_cls(ot)
            if type(self) != t:
                raise ETYPE(type(self), t)
            try:
                del val.__dict__["stamp"]
            except KeyError:
                pass
            self.update(val.__dict__)
        return self

    def merge(self, o, vals={}):
        """
            merge method.
            
            merge another object into this one (skip empty values).
            
        """
        return self.update(strip(self, vals))

    @locked(lock)
    def save(self):
        """
            save method.
            
            save the object to disk.
            
        """
        assert workdir
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        logging.debug("save %s" % self._path)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
        return self._path

    def search(self, match=None):
        """
            search method.
            
            see if one of the attributes values matches.
            
        """
        res = False
        if not match:
            return res
        for key, value in match.items():
            val = self.get(key, None)
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

    def set(self, k, v):
        """
             set method.
             
             set a attribute on the object.
             
        """
        self[k] = v


class Default(Object):

    """ 
        default class.
        
        overwritten getattribute to do autoinitialisation with a default value.
        
    """

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]

class Cfg(Default):

    """
        config class.
        
        default config class.
        
    """
    pass

# funcions

def stamp(o):
    """
        stamp function.
        
        add the filename as a stamp to objects so recursive object can be reconstructed properly.
        
    """

    for k in dir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def strip(o, vals=["",]):
    """
        strip function.

        return stripped version of the object (remove all empty fields).

    """
    rip = []
    for k in o:
        for v in vals:
            if k == v:
                rip.append(k)
    for k in rip:
        del o[k]
    return o
