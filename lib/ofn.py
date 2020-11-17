"object functions (ofn)"

from obj import get, items, get_type

def edit(o, setter, skip=False):
    "update an object from a dict"
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

def format(o, keys=[], skip=[]):
    "return 1 line output string"
    if not keys:
        keys = vars(o).keys()
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

def mkstamp(o):
    timestamp = str(datetime.datetime.now()).split()
    return os.path.join(get_type(self), str(uuid.uuid4()), os.sep.join(timestamp))

def ojson(o, *args, **kwargs):
    "return jsonified string"
    return json.dumps(o, default=default, *args, **kwargs)

def scan(o):
    for _k, v in items(o):
        if txt in str(v):
            return True
    return False

def search(o, s):
    "search object for a key,value to match dict"
    ok = False
    for k, v in items(s):
        vv = get(o, k)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def xdir(o, skip=None):
    "return a dir(o) with keys skipped"
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
 