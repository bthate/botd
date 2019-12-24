# BOTLIB - Framework to program bots.
#
# rss feed fetcher.

import bl
import datetime
import os
import random
import time
import urllib

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def __dir__():
    return ("Cfg", "Feed", "Fetcher", "Rss", "Seen", "delete" ,"display", "feed", "fetch", "init", "rss")

def init():
    fetcher.start()
    return fetcher

class Cfg(bl.Cfg):

    def __init__(self):
        super().__init__()
        self.display_list = ["title", "link"]
        self.dosave = True

class Feed(bl.Default):

    pass

class Rss(bl.Persist):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(bl.Persist):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(bl.Persist):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.seen = Seen()
        self._thrs = []

    def display(self, o):
        if bl.cfg.debug:
            return 0
        result = ""
        try:
            dl = o.display_list
        except AttributeError:
            dl = []
        if not dl:
            dl = self.cfg.display_list
        for key in dl:
            data = bl.get(o, key, None)
            if key == "link":
                datatmp = bl.utl.get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            if data:
                data = data.replace("\n", " ")
                data = bl.utl.strip_html(data.rstrip())
                data = bl.utl.unescape(data)
                result += data.rstrip()
                result += " - "
        return result[:-2].rstrip()

    def fetch(self, obj):
        if bl.cfg.debug:
            return 0
        counter = 0
        objs = []
        if not obj.rss:
            return 0
        for o in reversed(list(get_feed(obj.rss))):
            if not o:
                continue
            feed = Feed()
            bl.update(feed, o)
            bl.update(feed, obj)
            u = urllib.parse.urlparse(feed.link)
            url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            if url in self.seen.urls:
                continue
            self.seen.urls.append(url)
            counter += 1
            objs.append(feed)
            if self.cfg.dosave:
                try:
                    date = file_time(bl.tms.to_time(feed.published))
                except:
                    date = False
                if date:
                    feed.save(stime=date)
                else:
                    feed.save()
        self.seen.save()
        for o in objs:
            bl.fleet.announce(self.display(o))
        return counter

    def join(self):
        for thr in self._thrs:
            thr.join()

    def run(self):
        res = []
        thrs = []
        for o in bl.db.all("bl.rss.Rss"):
            thrs.append(bl.launch(self.fetch, o))
        for thr in thrs:
            res.append(thr.join())
        return res

    def start(self, repeat=True):
        bl.last(self.cfg)
        bl.last(self.seen)
        if repeat:
            repeater = bl.clk.Repeater(600, self.run)
            repeater.start()
            return repeater

    def stop(self):
        self.seen.save()

fetcher = Fetcher()

def get_feed(url):
    result = ""
    if bl.cfg.debug:
        return [bl.Object(), bl.Object()]
    result = bl.utl.get_url(url).data
    if gotparser:
        result = feedparser.parse(result)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [bl.Object(), bl.Object()]
    
def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def del(event):
    if not event.args:
        event.reply("delete <match>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for rss in bl.db.find("bl.rss.Rss", selector):
        nr += 1
        rss._deleted = True
        got.append(rss)
    for rss in got:
        rss.save()
    event.reply("ok %s" % nr)

def dpl(event):
    if len(event.args) < 2:
        event.reply("display <feed> key1,key2,etc.")
        return
    nr = 0
    setter = {"display_list": event.args[1]}
    for o in bl.db.find("bl.rss.Rss", {"rss": event.args[0]}):
        nr += 1
        bl.edit(o, setter)
        o.save()
    event.reply("ok %s" % nr)

def feed(event):
    match = ""
    if event.args:
        match = event.args[0]
    nr = 0
    diff = time.time() - bl.tms.to_time(bl.tms.day())
    res = list(bl.db.find("bl.rss.Feed", {"link": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s - %s" % (nr, o.title, o.summary, o.updated or o.published or "nodate", o.link))
        nr += 1
    if nr:
        return
    res = list(bl.db.find("bl.rss.Feed", {"title": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    res = list(bl.db.find("bl.rss.Feed", {"summary": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    if not nr:
        event.reply("no results found")
 
def ftc(event):
    res = fetcher.run()
    event.reply("fetched %s" % ",".join([str(x) for x in res]))

def rss(event):
    if not event.rest or "http" not in event.rest:
        nr = 0
        res = list(bl.db.find("bl.rss.Rss", {"rss": ""}))
        if res:
            for o in res:
                event.reply("%s %s" % (nr, o.rss))
                nr += 1
        else:
            event.reply("rss <url>")
        return
    o = Rss()
    o.rss = event.rest
    o.save()
    event.reply("ok 1")
