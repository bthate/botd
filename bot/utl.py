# BOTLIB - utl.py
#
# this file is placed in the public domain

"utilities (utl)"

# imports

import datetime
import importlib
import os
import pwd
import random
import re
import socket
import sys
import time
import traceback
import urllib

from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

# defines

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
    "%d, %b %Y %H:%M:%S +0000"
]

# exceptions

class ENOCLASS(Exception):

    "class not found"

# functions

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

def day():
    "this day"
    return str(datetime.datetime.today()).split()[0]

def direct(name, pname=''):
    "load module"
    return importlib.import_module(name, pname)

def file_time(timestamp):
    "filename from timestramp"
    s = str(datetime.datetime.fromtimestamp(timestamp))
    return s.replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def fntime(daystr):
    "time from filename"
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
    "class"
    try:
        modname, clsname = name.rsplit(".", 1)
    except Exception as ex:
        raise ENOCLASS(name) from ex
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_exception(txt="", sep=" "):
    "trace"
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        res = []
        for x in elem[0].split(os.sep)[::-1]:
            if x in ["bot"]:
                break
            res.append(x)
        result.append("%s:%s" % (os.sep.join(res[::-1]), elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

def get_tinyurl(url):
    "tinyurl"
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
    return []

def get_url(url):
    "http page"
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def locked(l):
    "lock descriptor"
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockeddec.__doc__ = func.__doc__
        return lockedfunc
    return lockeddec

def mods(mn, name="bot"):
    "modules in a package"
    mod = []
    pkg = direct(mn)
    path = pkg.__file__ or pkg.__path__[0]
    for m in ["%s.%s" % (name, x.split(os.sep)[-1][:-3]) for x in os.listdir(path)
              if x.endswith(".py")
              and not x == "setup.py"]:
        mod.append(direct(m))
    return mod

def privilege(name):
    "lower privileges"
    if os.getuid() != 0:
        return
    pwnam = pwd.getpwnam(name)
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    old_umask = os.umask(0o22)

def spl(txt):
    "comma splitted values"
    return iter([x for x in txt.split(",") if x])

def strip_html(text):
    "strip html from a page"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def to_time(daystr):
    "timestring to unix timestamp"
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
            break
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    return res

def toudp(host, port, txt):
    "send text to the udp to irc relay"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))

def unescape(text):
    "unescape html codes"
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    "useragent used when fetching http"
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTLIB +http://pypi.org/project/botlib)'
