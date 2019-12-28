# BOTD - python3 IRC channel daemon.
#
# generic functions

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
