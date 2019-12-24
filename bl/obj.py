# BOTLIB - Framework to program bots.
#
# big O Object.

import bl
import json

class Object:

    __slots__ = ("__dict__", "__path__", "_type")

    def __init__(self):
        super().__init__()
        self._type = bl.typ.get_type(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return json.dumps(self, default=default, indent=4, sort_keys=True)

    def json(self):
        return json.dumps(self, default=default, sort_keys=True)

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

def edit(o, setter):
    if not setter:
        setter = {}
    count = 0
    for key, value in items(setter):
        count += 1
        if "," in value:
            value = value.split(",")
        if value in ["True", "true"]:
            set(o, key, True)
        elif value in ["False", "false"]:
            set(o, key, False)
        else:
            set(o, key, value)
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
        val = get(o, key, None)
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

def get(o, key, default=None):
    try:
        return o[key]
    except (TypeError, KeyError):
        try:
            return o.__dict__[key]
        except (AttributeError, KeyError):
            return getattr(o, key, default)

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

def set(o, key, val):
    setattr(o, key, val)

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

def typed(o):
    return update(type(o)(), o)

def update(o1, o2, keys=None, skip=False):
    if not o2:
        return o1
    for key in o2:
        val = get(o2, key)
        if keys and key not in keys:
            continue
        if skip and not val:
            continue
        set(o1, key, val)

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
