# BOTD - 24/7 channel daemon (rss.py)
#
# this file is placed in the public domain

"rich site syndicate (rss)"

# imports

import datetime
import os
import random
import re
import time
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from bot.clk import Repeater
from bot.dbs import all, find, last
from bot.obj import Cfg, Default, O, Object, edit, save, get, update
from bot.hdl import Bus, debug
from bot.thr import launch
from bot.utl import get_url, strip_html, unescape, useragent

# defines

def __dir__():
    return ("Cfg", "Rss", "Feed", "Fetcher", "init")

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def init(hdl):
    "start a rss poller"
    f = Fetcher()
    return launch(f.start)

# classes

class Cfg(Cfg):

    "rss configuration"

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(Default):

    "feed item"

class Rss(Object):

    "rss feed url"

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    "all urls seen"

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    "rss feed poller"

    cfg = Cfg()
    seen = Seen()

    def display(self, o):
        "display a rss feed item"
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = get(o, key, None)
            if not data:
                continue
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            data = data.replace("\n", " ")
            data = strip_html(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        "rss feed"
        counter = 0
        objs = []
        if not rssobj.rss:
            return 0
        for o in reversed(list(get_feed(rssobj.rss))):
            if not o:
                continue
            f = Feed()
            update(f, rssobj)
            update(f, O(o))
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                save(f)
        if objs:
            save(Fetcher.seen)
        for o in objs:
            txt = self.display(o)
            Bus.announce(txt)
        return counter

    def run(self):
        "all feeds"
        thrs = []
        for fn, o in all("bot.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        "rss poller"
        last(Fetcher.cfg)
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        "rss poller"
        save(self.seen)

# functions

def get_feed(url):
    "feed"
    if debug:
        return [Object(), Object()]
    try:
        result = get_url(url)
    except (HTTPError, URLError):
        return [Object(), Object()]
    if gotparser:
        result = feedparser.parse(result.data)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [Object(), Object()]
