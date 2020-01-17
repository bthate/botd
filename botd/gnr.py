# BOTD - python3 IRC channel daemon.
#
# generic functios.

"""
    generic functions.

    functions that operate on a object.
    
"""

import json
import _thread

from botd.utl import locked

lock = _thread.allocate_lock()

# functions

def edit(o, setter):
    """
        edit function.
        
        the edit command can be used to change items of an object.
        
    """
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
    """
        format function.
        
        the format function return a displayable string of an object.
        
    """
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
    """
        get function
        
        returns a the value of an object attribute.
        
    """
    try:
        return o[k]
    except KeyError:
        return d

def items(o):
    """
        items function
        
        return all items of an object.
        
    """
    return o.__dict__.items()

def keys(o):
    """
        keys function
        
        return all attribute names of an object.
        
    """
    return o.__dict__.keys()

def last(o):
    """
        last function.
        
        return last saved version of an object's type
        
    """
    from botd.dbs import Db
    db = Db()
    return db.last(str(get_type(o)))

@locked(lock)
def load(o, path):
    """
        load function.
        
        load an object from disk
        
    """
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
    """
        merge function

        the merge function merges 2 objects into one, not updating a field if the value is empty.
        
    """
    return update(o1, strip(o2))

@locked(lock)
def save(o):
    """
        save function
        
        save an object to disk

    """
    assert workdir
    opath = os.path.join(workdir, "store", o._path)
    cdir(opath)
    logging.debug("save %s" % o._path)
    with open(opath, "w") as ofile:
        json.dump(stamp(o), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
    return o._path

def search(o, match=None):
    """
        search function.
        
        search an object and check if match, a key/value dict matches.
        
    """
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
    """
        set function.
        
        set attribute of an object to a new value.
        
    """
    o[k] = v

def setter(o, d):
    """
        setter function
        
        the setter function updates an object with the provided key/value dict.
        
    """
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
    """
        sliced function.
        
        sliced returns a sliced version (only has keys attributes) of an object.
        
    """
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
    """
        stamp function.
        
        the stamp function add a "stamp" field to the object's sub object's so it can be properly reconstructed.
        this field get's removed when loading an object from disk.
         
    """
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
    """
        strip function.
        
        strip empty fields from an object.

    """
    for k in o:
       if not k:
          del o[k]
    return o

def to_json(o):
    """
        to_json function.

        return a json string dump of an object.
        
    """
    return json.dumps(o, cls=ObjectEncoder, indent=4, sort_keys=True)

def update(o1, o2, keys=None, skip=None):
    """
        update function.
        
        update one object with the other.

    """
    for key in o2:
        if keys and key not in keys:
            continue
        if skip and key in skip:
            continue
        set(o1, key, get(o2, key))

def values(o):
    """
        values function.
        
        return all values of an object.
        
    """
    return o.__dict__.values()

def xdir(o, skip=""):
    """
        xdir function.
        
        run dir() and skip keys that match with 'skip'
        
    """  
    res = []
    for k in dir(o):
        if skip and skip in k:
            continue
        res.append(k)
    return res
