# BOTD - python3 IRC channel daemon.
#
# rss feed fetcher.

import datetime
import os
import random
import time
import urllib

from botd.clk import Repeater
from botd.dbs import Db
from botd.flt import Fleet
from botd.obj import Cfg, Object
from botd.tms import to_time
from botd.thr import launch
from botd.tms import to_time, day
from botd.utl import get_tinyurl, get_url, strip_html, unescape

from botd.krn import kernels

# defines

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def __dir__():
    return ("Cfg", "Feed", "Fetcher", "Rss", "Seen", "delete" ,"display", "feed", "fetch", "init", "rss")

def init(kernel):
    k = kernels.get_first()
    k.run.fetcher = Fetcher()
    k.run.fetcher.start()
    return k.run.fetcher

# classes

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.display_list = "title,link"
        self.dosave = True
        self.tinyurl = True

class Feed(Object):

    pass

class Rss(Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    cfg = Cfg()
    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []

    def display(self, o):
        result = ""
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            dl = []
        if not dl:
            dl = self.cfg.display_list.split(",")
        for key in dl:
            if not key:
                continue
            data = o.get(key, None)
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            if data:
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = unescape(data)
                result += data.rstrip()
                result += " - "
        return result[:-2].rstrip()

    def fetch(self, obj):
        k = kernels.get_first()
        counter = 0
        objs = []
        if not obj.rss:
            return 0
        for o in reversed(list(get_feed(obj.rss))):
            if not o:
                continue
            feed = Feed()
            feed.update(obj)
            feed.update(o)
            u = urllib.parse.urlparse(feed.link)
            url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(feed)
            if self.cfg.dosave:
                feed.save()
        if objs:
            Fetcher.seen.save()
        for o in objs:
            k.fleet.announce(self.display(o))
        return counter

    def join(self):
        res = []
        remove = []
        for thr in self._thrs:
            res.append(thr.join())
            remove.append(thr)
        for thr in remove:
            self._thrs.remove(thr)
        return res

    def run(self):
        res = []
        thrs = []
        db = Db()
        for o in db.all("botd.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        for thr in thrs:
            res.append(thr.join())
        return res

    def start(self, repeat=True):
        Fetcher.cfg.last()
        Fetcher.seen.last()
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

# functions

def get_feed(url):
    result = get_url(url)
    if gotparser:
        result = feedparser.parse(result)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [Object(), Object()]
    
def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

