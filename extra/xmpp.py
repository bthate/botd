""" XMPP bot for botd. """

__version__ = 1

import getpass
import logging
import ssl
import sys
import threading
import _thread

from bl.err import EINIT
from bl.evt import Event
from bl.krn import dispatch
from bl.obj import Object
from bl.pst import Cfg, Persist

from botd.bot import Bot, Event
from botd.flt import Fleet
from botd.usr import Users

def __dir__():
    return ("XMPP", "Event", "Cfg", "init", "stripped")

fleet = Fleet()
users = Users()

def init(cfg):
    bot = XMPP()
    bot.cfg.last()
    if cfg.prompting:
        try:
            bot.cfg.user = cfg.args[0]
            if cfg.prompting or not bot.cfg.password:
                bot.cfg.password = getpass.getpass()
            bot.cfg.save()
        except (ValueError, IndexError):
            sys.stdout.write("%s <JID>" % cfg.name)
            sys.stdout.flush()
            raise EINIT
    bot.start()
    return bot

try:
    import sleekxmpp
except ImportError:
    pass

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.ipv6 = False
        self.nick = ""
        self.noresolver = True
        self.password = ""
        self.server = ""
        self.user = ""

class Event(Event):

    def __init__(self):
        super().__init__()
        self.cc = ""
        self.channel = ""
        self.element = ""
        self.jid = ""
        self.nick = ""
        self.server = ""
        self.mtype = ""
        self.txt = ""

class XMPP(Bot):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = True
        self.cc = ""
        self.cfg = Cfg()
        self.channels = []
        self.client = None
        self.jid = None
        self.rooms = []
        self.state = Object()

    def _bind(self, data):
        self.jid = str(data)

    def _connect(self, user, pw):
        self._makeclient(user, pw)
        if self.cfg.noresolver:
            self.client.configure_dns(None)
        self.client.connect(use_tls=True)
        self._connected.set()

    def _fileno(self):
        return self.client.filesocket.fileno()
        
    def _makeclient(self, jid, password):
        self.client = sleekxmpp.clientxmpp.ClientXMPP(jid,
                                                      password,
                                                      plugin_config={},
                                                      plugin_whitelist=[],
                                                      escape_quotes=False,
                                                      sasl_mech=None)
        self.client._error = Object()
        self.client.register_plugin(u'xep_0045')
        self.client.add_event_handler('errored', self.handled)
        self.client.add_event_handler('failed_auth', self.handled)
        self.client.add_event_handler("message", self.messaged)
        self.client.add_event_handler("iq", self.handled)
        self.client.add_event_handler('presence', self.presenced)
        self.client.add_event_handler('presence_dnd', self.presenced)
        self.client.add_event_handler('presence_xa', self.presenced)
        self.client.add_event_handler('presence_available', self.presenced)
        self.client.add_event_handler('presence_chat', self.presenced)
        self.client.add_event_handler('presence_away', self.presenced)
        self.client.add_event_handler('presence_unavailable', self.presenced)
        self.client.add_event_handler('presence_subscribe', self.presenced)
        self.client.add_event_handler('presence_subscribed', self.presenced)
        self.client.add_event_handler('presence_unsubscribe', self.presenced)
        self.client.add_event_handler('presence_unsubscribed', self.presenced)
        self.client.add_event_handler("session_bind", self._bind)
        self.client.add_event_handler("session_start", self._start)
        self.client.add_event_handler("ssl_invalid_cert", self.handled)
        self.client.exception = self.handled
        self.client.reconnect_max_attempts = 3
        self.client.ssl_version = ssl.PROTOCOL_SSLv23
        self.client.use_ipv6 = self.cfg.ipv6


    def _start(self, data):
        try:
            self.client.send_presence()
            self.client.get_roster()
        except sleekxmpp.exceptions.IqTimeout:
            self.reconnect()

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt, "chat")
        #for room in self.rooms:
        #    self.say(channel, txt, "groupchat")

    def connect(self, user="", password=""):
        self._connect(user, password)
        return True

    def join(self, room, nick="obot"):
        if room not in self.rooms:
            self.rooms.append(room)
        self._connected.wait()
        self.client.plugin['xep_0045'].joinMUC(room,
                                               nick,
                                               wait=True)

    def say(self, channel, txt, mtype="chat"):
        try:
            sleekxmpp.jid.JID(channel)
        except sleekxmpp.jid.InvalidJID:
            return
        if self.cfg.user in channel:
            return
        if channel in self.rooms:
            mtype = "groupchat"
        if mtype == "groupchat":
            channel = stripped(channel)
        self.client.send_message(channel, str(txt), mtype)

    def sleek(self):
        self.client.process(block=True)

    def stop(self):
        if "client" in self and self.client:
            self.client.disconnect()
        super().stop()

    def start(self):
        fleet.add(self)
        ok = self.connect(self.cfg.user, self.cfg.password)
        if ok:
            if self.cfg.channel:
                self.join(self.cfg.channel, self.cfg.nick)
        launch(self.sleek)
        return self

    def handled(self, data):
        print(data)

    def messaged(self, data):
        if '<delay xmlns="urn:xmpp:delay"' in str(data):
            return
        origin = str(data["from"])
        if data["type"] == "groupchat":
            if not users.allowed(origin, "USER"):
                return
        txt = data["body"]
        m = Event()
        m.parse(txt)
        m.txt = txt
        m.jid = origin
        m.orig = repr(self)
        m.origin = origin
        m.mtype = data["type"]
        if m.mtype == "error":
            loggin.error("error %s" % m.error)
            return
        m.nick = m.origin.split("/")[-1]
        m.user = m.jid = stripped(m.origin)
        m.channel = m.origin
        if self.cfg.user == m.user:
            return
        k.put(m)

    def presenced(self, data):
        o = Event()
        o.mtype = data["type"]
        o.orig = repr(self)
        o.cc = ""
        o.origin = str(data["from"])
        o.jid = o.origin
        o.nick = o.origin.split("/")[-1]
        o.server = self.cfg.server
        o.room = stripped(o.origin)
        o.user = stripped(o.origin)
        if "txt" not in o:
            o.txt = ""
        o.element = "presence"
        if self.cfg.user in o.origin:
            return
        if o.mtype == 'subscribe':
            pres = Event({'to': o.origin, 'type': 'subscribed'})
            self.client.send_presence(pres)
            pres = Event({'to': o.origin, 'type': 'subscribe'})
            self.client.send_presence(pres)
            if o.origin not in self.channels:
                self.channels.append(o.origin)
        elif o.mtype == "unsubscribe":
            if o.origin in self.channels:
                self.channels.remove(o.origin)
            return
        elif o.mtype == "available":
            if o.user not in self.channels:
                self.channels.append(o.user)
        elif o.mtype == "unavailable":
            if o.user in self.channels:
                self.channels.remove(o.user)

def stripped(jid):
    try:
        return str(jid).split("/")[0]
    except (IndexError, ValueError):
        return str(jid)
