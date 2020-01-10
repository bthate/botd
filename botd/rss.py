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
    fetcher = Fetcher()
    fetcher.start()
    return fetcher

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
        fetchers.add(self)

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
        for thr in self._thrs:
            thr.join()

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
            repeater = Repeater()
            repeater.start(600.0, self.run)
            return repeater

    def stop(self):
        Fetcher.seen.save()

class Fetchers(Object):

    fetchers = []
    
    def add(self, fetcher):
        Fetchers.fetchers.append(fetcher)

    def get_first(self):
        if Fetchers.fetchers:
            return Fetchers.fetchers[0]

# functions

def get_feed(url):
    result = get_url(url).data
    if gotparser:
        result = feedparser.parse(result)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [Object(), Object()]
    
def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def delete(event):
    if not event.args:
        event.reply("delete <match>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    db = Db()
    for rss in db.find("botd.rss.Rss", selector):
        nr += 1
        rss._deleted = True
        got.append(rss)
    for rss in got:
        rss.save()
    event.reply("ok %s" % nr)

def display(event):
    if len(event.args) < 2:
        event.reply("display <feed> key1,key2,etc.")
        return
    nr = 0
    db = Db()
    setter = {"display_list": event.args[1]}
    db = Db()
    for o in db.find("botd.rss.Rss", {"rss": event.args[0]}):
        nr += 1
        o.edit(setter)
        o.save()
    event.reply("ok %s" % nr)

def feed(event):
    match = ""
    if event.args:
        match = event.args[0]
    nr = 0
    diff = time.time() - to_time(day())
    db = Db()
    res = list(db.find("botd.rss.Feed", {"link": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s - %s" % (nr, o.title, o.summary, o.updated or o.published or "nodate", o.link))
        nr += 1
    if nr:
        return
    res = list(db.find("botd.rss.Feed", {"title": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    res = list(db.find("botd.rss.Feed", {"summary": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    if not nr:
        event.reply("no results found")
 
def fetch(event):
    fetcher = fetchers.get_first()
    if not fetcher:
        fetcher = Fetcher()
    res = fetcher.run()
    event.reply("fetched %s" % ",".join([str(x) for x in res]))

def rss(event):
    db = Db()
    if not event.args or "http" not in event.args[0]:
        nr = 0
        for o in db.find("botd.rss.Rss", {"rss": ""}):
            event.reply("%s %s" % (nr, o.rss))
            nr += 1
        if not nr:
            event.reply("rss <url>")
        return
    url = event.args[0]
    res = list(db.find("botd.rss.Rss", {"rss": url}))
    if res:
        event.reply("feed is already known.")
        return
    o = Rss()
    o.rss = event.args[0]
    o.save()
    event.reply("ok 1")

# runtime

fetchers = Fetchers()
