# BOTD - IRC channel daemon.
#
# rss feed fetcher commands

""" fetches rss feeds and echo's them on a channel. """

from botd.dbs import Db
from botd.krn import kernels
from botd.rss import Fetcher

# defines

def __dir__():
    return ("delete", "display", "feed", "fetch", "rss")

k = kernels.get_first()

# commands

def delete(event):
    """
        delete <string to match with feed url.>
        
        deletes a rss entry so it won't display any more.
        
    """
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
    """
        display <feed> <key1,key2,key3>
 
        set the feeds item to display to key1,key2 and key3. feed is a string matching the url of the feed.
        
    """
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
    """
        feed <match>
        
        search saved feeds for items that have fields with data in them that matches the match string.
        
    """
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
    """
        fetch command
        
        run one round of fetching the feeds.
        
    """
    if not k.run.fetcher:
        k.run.fetcher = Fetcher()
    k.run.fetcher.start(False)
    res = k.run.fetcher.run()
    event.reply("fetched %s" % ",".join([str(x) for x in res]))

def rss(event):
    """
        rss <url>
        
        saves a feed url to disk.
        
    """
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
