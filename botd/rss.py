# BOTD - the 24/7 channel daemon !
#
#

import datetime, html.parser, os, random, re, time, urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from bot.cfg import Cfg
from bot.clk import Repeater
from bot.dbs import Db
from bot.dft import Default
from bot.krn import k
from bot.obj import Object
from bot.opr import edit
from bot.tsk import launch
from bot.tms import to_time, day

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

debug = False

def init(k):
    f = Fetcher()
    f.start()
    return f

class Cfg(Cfg):

    pass

class Feed(Default):

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
            f = Feed()
            f.update(obj)
            f.update(o)
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
                f.save()
        if objs:
            Fetcher.seen.save()
        for o in objs:
            k.fleet.announce(self.display(o))
        return counter

    def run(self):
        thrs = []
        db = Db()
        for o in db.all("botd.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        Fetcher.cfg.last()
        Fetcher.seen.last()
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

def file_time(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def get_feed(url):
    if debug:
        return [Object(), Object()]
    try:
        result = get_url(url)
    except (HTTPError, URLError):
        return [Object(), Object()]
    if gotparser:
        res = feedparser.parse(result.data)
        if "entries" in res:
            for entry in res["entries"]:
                yield entry
    else:
        print("feedparser is missing")
        return [Object(), Object()]

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
    return []

def get_url(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def unescape(text):
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTD +http://git@bitbucket.org/bthate/botd)'

def rm(event):
    if not event.args:
        event.reply("rm <match>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    db = Db()
    for o in db.find("botd.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        o.save()
    event.reply("ok")

def display(event):
    if len(event.args) < 2:
        event.reply("display <feed> key1,key2,etc.")
        return
    nr = 0
    setter = {"display_list": event.args[1]}
    db = Db()
    for o in db.find("botd.rss.Rss", {"rss": event.args[0]}):
        nr += 1
        edit(o, setter)
        o.save()
    event.reply("ok")

def feed(event):
    if not event.args:
        event.reply("feed <match>")
        return
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
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return
    event.reply("no feeds registered.")

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
    event.reply("ok")
