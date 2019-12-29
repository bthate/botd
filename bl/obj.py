# BOTD - python3 IRC channel daemon.
#
# big O Object.

import bl
import json

from bl.typ import get_type

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
        val = db.last(str(bl.typ.get_type(o)))
        if val:
            o.update(val)
            o.__path__ = val.__path__
            return o.__path__

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
