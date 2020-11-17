"rich site syndicate"

import datetime, os, random, re, time, urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from bus import bus
from clk import Repeater
from dbs import all, find, last, lastmatch
from obj import Cfg, Default, O, Object, save, get, update
from ofn import edit
from hdl import debug
from thr import launch

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

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


def init(hdl):
    "start a rss poller and return it"
    f = Fetcher()
    return launch(f.start)

class Cfg(Cfg):

    "rss configuration"

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(Default):

    "a feed item"

class Rss(Object):

    "a rss feed url"

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
        "update a rss feed"
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
            bus.announce(txt)
        return counter

    def run(self):
        "update all feeds"
        thrs = []
        for fn, o in all("rss.Rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        "start the rss poller"
        last(Fetcher.cfg)
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        "stop the rss poller"
        save(self.seen)

fetcher = Fetcher()

def get_feed(url):
    "return a feed by it's url"
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
        print("feedparser is missing")
        return [Object(), Object()]

def file_time(timestamp):
    s = str(datetime.datetime.fromtimestamp(timestamp))
    return s.replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def get_tinyurl(url):
    "return a corresponding timyurl"
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
    "return a http page"
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def strip_html(text):
    "strip html codes from a page"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def to_time(daystr):
    "convert a timestring to unix timestamp"
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

def unescape(text):
    "unescape html codes"
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    "return useragent"
    return 'Mozilla/5.0 (X11; Linux x86_64) OBJ +http://pypi.org/bthate/obj)'

def rem(event):
    "remove a rss feed"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in find("rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")

def dpl(event):
    "set keys to display"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in lastmatch("rss.Rss", {"rss": event.args[0]}):
        edit(o, setter)
        save(o)
        event.reply("ok")

def ftc(event):
    "manual run a fetch batch"
    res = []
    thrs = []
    fetchr = Fetcher()
    fetchr.start(False)
    thrs = fetchr.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rss(event):
    "add a feed"
    if not event.args:
        return
    url = event.args[0]
    res = list(find("rss.Rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    save(o)
    event.reply("ok")
