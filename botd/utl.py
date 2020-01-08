# BOTD - python3 IRC channel daemon.
#
# utility functions.

import json
import html
import html.parser
import logging
import os
import random
import re
import stat
import string
import types
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode, urlunparse
from urllib.request import Request, urlopen

from botd.trc import get_exception

# defines

def __dir__():
    return ("cdir", "check_permissions", "consume", "fromfile", "get_name", "get_tinyurl", "get_url", "hd", "kill", "fnlast", "locked", "match", "randomname", "strip_html", "touch", "useragent", "unescape") 

allowedchars = string.ascii_letters + string.digits + '_+/$.-'
resume = {}

# functions

def cdir(path):
    if os.path.exists(path):
        return
    res = ""
    path2, fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass
    return True

def check_permissions(path, dirmask=0o700, filemask=0o600):
    uid = os.getuid()
    gid = os.getgid()
    try:
        stats = os.stat(path)
    except FileNotFoundError:
        return
    except OSError:
        dname = os.path.dirname(path)
        stats = os.stat(dname)
    if stats.st_uid != uid:
        os.chown(path, uid, gid)
    if os.path.isfile(path):
        mask = filemask
    else:
        mask = dirmask
    mode = oct(stat.S_IMODE(stats.st_mode))
    if mode != oct(mask):
        os.chmod(path, mask)

def consume(elems):
    fixed = []
    for e in elems:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue

def edit(o, setter):
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

def fromfile(f):
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return json.load(f, object_hook=botd.hook)
    except:
        fcntl.flock(f, fcntl.LOCK_UN)
        raise

def get_name(o):
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

def get_tinyurl(url):
    postarray = [
        ('submit', 'submit'),
        ('url', url),
        ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php', data=bytes(postdata, "UTF-8"))
    req.add_header('User-agent', useragent())
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()

def get_url(*args):
    logging.debug("GET %s" % args[0])
    url = urlunparse(urllib.parse.urlparse(args[0]))
    req = Request(url, headers={"User-Agent": useragent()})
    resp = urlopen(req)
    resp.data = resp.read()
    return resp

def hd(*args):
    homedir = os.path.expanduser("~")
    return os.path.abspath(os.path.join(homedir, *args))

def kill(thrname):
    for task in threading.enumerate():
        if thrname not in str(task):
            continue
        if "cancel" in dir(task):
            task.cancel()
        if "exit" in dir(task):
            task.exit()
        if "stop" in dir(task):
            task.stop()

def fnlast(otype):
    fns = list(names(otype))
    if fns:
        return fns[-1]

def locked(lock):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res
        return lockedfunc
    return lockeddec

def match(a, b):
    for n in b:
        if n in a:
            return True
    return False        

def randomname():
    s = ""
    for x in range(8):
        s += random.choice(allowedchars)
    return s

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def useragent():
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTD +http://git@github.com/bthate/botd)'
    
def unescape(text):
    import html
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def xdir(o, skip=""):
    res = []
    for k in dir(o):
        if skip and skip in k:
            continue
        res.append(k)
    return res
