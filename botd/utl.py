# BOTD - IRC channel daemon.
#
# utility functions.

""" utility functions. """

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

from botd.err import EDEBUG
from botd.trc import get_exception

# defines

def __dir__():
    return ("cdir", "check_permissions", "consume", "get_name", "get_tinyurl", "get_url", "hd", "kill", "fnlast", "locked", "strip_html", "touch", "useragent", "unescape") 

allowedchars = string.ascii_letters + string.digits + '_+/$.-'
resume = {}

# functions

def cdir(path):
    """
        cdir function.
        
        create a directory.
        
    """
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
    """
        check_permssion function.
        
        set permissions of a file.
        
    """
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
    """
        consume functions.
        
        wait for all elements.
        
    """
    fixed = []
    for e in elems:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue

def get_name(o):
    """
        get_name function.
        
        return the FQN (full qualified name) of a object.
        
    """
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
    """
        get_tinyurl function.
        
        return a tinyurl version of an url.
        
    """
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
    """
        get_url function.
        
        return a http get on a url.
        
    """
    from botd.krn import kernels
    k = kernels.get_first()
    if k.cfg.debug:
        logging.debug("debug enabled, ignoring %s" % args[0])
        return ""
    logging.debug("GET %s" % args[0])
    url = urlunparse(urllib.parse.urlparse(args[0]))
    req = Request(url, headers={"User-Agent": useragent()})
    data = ""
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    return data

def hd(*args):
    """
        hd function.
        
        return the homedirectory appended with arguments.
        
    """
    homedir = os.path.expanduser("~")
    return os.path.abspath(os.path.join(homedir, *args))

def kill(thrname):
    """
        kill function.
        
        kill all threads matching threadname.
        
    """
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
    """
        fnlast function.
        
        return the filename of the last object of object type.
        
    """
    fns = list(names(otype))
    if fns:
        return fns[-1]

def locked(lock):
    """
        locked funcion.
        
        locked decorator to use on methods or functions.
        
    """
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

def strip_html(text):
    """
        strip_html function.
        
        strip html code  from text.
        
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def touch(fname):
    """
        touch function.
        
        touch a filename and thus create it.
        
    """
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def useragent():
    """
        useragent function
        
        return the useragent to use if http requestt.
        
    """
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTD +http://git@bitbucket.org/botd/botd)'
    
def unescape(text):
    """
        unescape function.
        
        remove escape code from text.
        
    """
    import html
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def xdir(o, skip=""):
    """
        xdir function.
        
        return results of the dir() function but skip keys containing skip characters.
        
    """
    res = []
    for k in dir(o):
        if skip and skip in k:
            continue
        res.append(k)
    return res

def xobj(obj, skip="", types=[]):
    """
        xobj function.
        
        return the objects matching skipped keys.
        
    """
    res = []
    for k in xdir(obj, skip):
        o = getattr(obj, k, None)
        ok = False
        for t in types:
            if t == type(o):
                ok = True
        if types and not ok:
            continue
        if o:
            res.append(o)
    return res
    