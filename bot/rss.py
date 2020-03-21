# BOTLIB - Framework to program bots.
#
#

import bot
import lo
import lo.clk
import lo.tms
import logging
import re
import time
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode, urlunparse
from urllib.request import Request, urlopen

from bot import k

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    logging.debug("feedparser is not found")
    gotparser = False

def __dir__():
    return ("Cfg,", "Feed", "Rss", "Seen", "Fetcher", "delete", "display", "feed", "fetch", "init", "rss")

def init(kernel):
    fetcher = Fetcher()
    fetcher.start()
    return fetcher

class Cfg(lo.Object):

    def __init__(self):
        super().__init__()
        self.display_list = "title,link"
        self.dosave = True
        self.tinyurl = False

class Feed(lo.Object):

    pass

class Rss(lo.Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(lo.Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(lo.Object):

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

    def run(self):
        thrs = []
        db = lo.Db()
        for o in db.all("bot.rss.Rss"):
            thrs.append(k.launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        Fetcher.cfg.last()
        Fetcher.seen.last()
        if repeat:
            repeater = lo.clk.Repeater(300.0, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def get_feed(url):
    if lo.cfg.debug:
        return [lo.Object(), lo.Object()]
    result = get_url(url)
    if gotparser:
        res = feedparser.parse(result.data)
        if "entries" in res:
            for entry in res["entries"]:
                yield entry
    else:
        logging.debug("feedparser is missing")
        return [lo.Object(), lo.Object()]

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

def get_url(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def unescape(text):
    import html
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTLIB +http://git@bitbucket.org/botd/botlib)'

def delete(event):
    if not event.args:
        event.reply("delete <match>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    db = lo.Db()
    for rss in db.find("bot.rss.Rss", selector):
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
    setter = {"display_list": event.args[1]}
    db = lo.Db()
    for o in db.find("bot.rss.Rss", {"rss": event.args[0]}):
        nr += 1
        o.edit(setter)
        o.save()
    event.reply("ok %s" % nr)

def feed(event):
    if not event.args:
        event.reply("feed <match>")
        return
    match = event.args[0]
    nr = 0
    diff = time.time() - lo.tms.to_time(lo.tms.day())
    db = lo.Db()
    res = list(db.find("bot.rss.Feed", {"link": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s - %s" % (nr, o.title, o.summary, o.updated or o.published or "nodate", o.link))
        nr += 1
    if nr:
        return
    res = list(db.find("srv.rss.Feed", {"title": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    res = list(db.find("bot.rss.Feed", {"summary": match}, delta=-diff))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    if not nr:
        event.reply("no results found")
 
def fetch(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join())
    event.reply("fetched %s" % ",".join([str(x) for x in res]))

def rss(event):
    db = lo.Db()
    if not event.args or "http" not in event.args[0]:
        nr = 0
        for o in db.find("bot.rss.Rss", {"rss": ""}):
            event.reply("%s %s" % (nr, o.rss))
            nr += 1
        if not nr:
            event.reply("rss <url>")
        return
    url = event.args[0]
    res = list(db.find("bot.rss.Rss", {"rss": url}))
    if res:
        event.reply("feed is already known.")
        return
    o = Rss()
    o.rss = event.args[0]
    o.save()
    event.reply("ok 1")
