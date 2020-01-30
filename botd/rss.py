# BOTD - IRC channel daemon.
#
# rss feed fetcher.

""" fetches rss feeds and echo's them on a channel. """

import datetime
import os
import random
import time
import urllib

from botd.clk import Repeater
from botd.krn import kernels
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
    return ("Cfg", "Feed", "Fetcher", "Rss", "Seen", "init")

k = kernels.get_first()

def init(kernel):
    """
        init function.
        
        start the rss fetcher.
        
    """
    k.run.fetcher = Fetcher()
    k.run.fetcher.start()
    return k.run.fetcher

# classes

class Cfg(Cfg):

    """
        rss config class
        
        provides rss configuration data.
        
    """

    def __init__(self):
        super().__init__()
        self.display_list = "title,link"
        self.dosave = True
        self.tinyurl = True

class Feed(Object):

    """
        feed class.
        
        represent one single feed item.
        
    """
    pass

class Rss(Object):

    """
        rss class.
        
        rss url entry.
        
    """

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    """
        seen class.
        
        holds a list of all seen urls.
        
    """
    
    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    """
        fetcher class.
        
        polls a list of rss urls periodically and displays new urls on the channel.
        
    """

    cfg = Cfg()
    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []

    def display(self, o):
        """
            display method
            
            return displayable string of the feed.
            
        """
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
        """
            fetch method
            
            fetch data from one feed.
            
        """
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

    def run(self):
        """
            run method
            
            do one run of fetching all the feeds and displaying them.
        
        """
        res = []
        thrs = []
        db = Db()
        for o in db.all("botd.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        for thr in thrs:
            res.append(thr.join(10.0))
        return res

    def start(self, repeat=True):
        """
            start method
            
            start the fetcher, polls after initial wait.
            
        """
        Fetcher.cfg.last()
        Fetcher.seen.last()
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()
            return repeater

    def stop(self):
        """
            stop method.
            
            save seen urls to disk.
            
        """
        Fetcher.seen.save()

# functions

def get_feed(url):
    """
        get_feed function
        
        fetch a rss feed from url.
        
    """
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
