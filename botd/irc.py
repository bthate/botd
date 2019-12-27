# BOTLIB - Framework to program bots.
#
# 

import logging
import os
import queue
import socket
import ssl
import sys
import textwrap
import time
import threading
import _thread

from bl.bot import Bot
from bl.dbs import last
from bl.err import EINIT
from bl.evt import Event
from bl.flt import Fleet
from bl.krn import dispatch
from bl.obj import Object
from bl.pst import Cfg
from bl.thr import launch
from bl.usr import Users
from bl.utl import locked

def __dir__():
    return ('Cfg', 'DCC', 'DEvent', 'Event', 'IRC', 'init', "errored", "noticed", "privmsged")

default = {
           "blocking": False,
           "channel": "",
           "nick": "botd",
           "ipv6": False,
           "port": 6667,
           "server": "",
           "sleep": 5.0,
           "ssl": False,
           "realname": "botd",
           "username": "botd",
          }

lock = _thread.allocate_lock()
fleet = Fleet()
users = Users()
          
def init(cfg):
    bot = IRC()
    last(bot.cfg)
    if cfg.prompting:
        try:
            server, channel, nick = cfg.args
            bot.cfg.server = server
            bot.cfg.channel = channel
            bot.cfg.nick = nick
            bot.cfg.save()
        except ValueError:
            raise EINIT("%s <server> <channel> <nick>" % cfg.name)
    bot.start()
    return bot

class Cfg(Cfg):

    pass

class Event(Event):

    def __init__(self):
        super().__init__()
        self.arguments = []
        self.cc = ""
        self.channel = ""
        self.command = ""
        self.nick = ""
        self.orig = ""
        self.target = ""

    def show(self):
        for txt in self.result:
            fleet.echo(self.orig, self.channel, txt)

class DEvent(Event):

    def __init__(self):
        super().__init__()
        self._sock = None
        self._fsock = None
        self.channel = ""

    def raw(self, txt):
        if self._fsock:
            self._fsock.write(str(txt) + "\n") 
            self._fsock.flush()

    def reply(self, txt):
        self.raw(txt)

    def show(self):
        for txt in self.result:
            fleet.echo(self.orig, self.channel, txt)

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 480

class IRC(Bot):

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self._threaded = False
        self.cc = "!"
        self.cfg = Cfg(default)
        self.channels = []
        self.state = Object()
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        if self.cfg.channel and self.cfg.channel not in self.channels:
            self.channels.append(self.cfg.channel)

    def _connect(self):
        if self.cfg.ipv6:
            oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(int(self.cfg.blocking or 1))
        oldsock.settimeout(5.0)
        logging.warn("connect %s:%s" % (self.cfg.server, self.cfg.port or 6667))
        oldsock.connect((self.cfg.server, int(self.cfg.port or 6667)))
        oldsock.setblocking(int(self.cfg.blocking or 1))
        oldsock.settimeout(700.0)
        if self.cfg.ssl:
            self._sock = ssl.wrap_socket(oldsock)
        else:
            self._sock = oldsock
        self._fsock = self._sock.makefile("r")
        fileno = self._sock.fileno()
        os.set_inheritable(fileno, os.O_RDWR)
        self._connected.set()
        return True

    def _parsing(self, txt):
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.orig = repr(self)
        o.txt = rawstr
        o.cc = self.cc
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                    o.txt = " ".join(txtlist)
        else:
            o.chk = o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        if o.arguments:
            o.target = o.arguments[-1]
        else:
            o.target = ""
        if o.target.startswith("#"):
            o.channel = o.target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        o.args = o.txt.split()
        o.rest = " ".join(o.args)
        return o

    @locked(lock)
    def _say(self, channel, txt, mtype="chat"):
        wrapper = TextWrap()
        for line in txt.split("\n"):
            for t in wrapper.wrap(line):
                self.command("PRIVMSG", channel, t)
                time.sleep(self.cfg.sleep)

    def _some(self, use_ssl=False, encoding="utf-8"):
        if use_ssl:
            inbytes = self._sock.read()
        else:
            inbytes = self._sock.recv(512)
        txt = str(inbytes, encoding)
        if txt == "":
            raise ConnectionResetError
        logging.info(txt.rstrip())
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self._say(channel, txt)

    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self):
        nr = 0
        while 1:
            self.state.nrconnect += 1
            logging.warning("connect #%s" % self.state.nrconnect)
            if self._connect():
                break
            time.sleep(nr * self.cfg.sleep)
            nr += 1
        self.logon(self.cfg.server, self.cfg.nick)

    def poll(self):
        self._connected.wait()
        if not self._buffer:
            try:
                self._some()
            except (ConnectionResetError, socket.timeout) as ex:
                e = Event()
                e._error = str(ex)
                e.chk = "ERROR"
                return e
        e = self._parsing(self._buffer.pop(0))
        cmd = e.command
        if cmd == "001":
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        elif cmd == "433":
            nick = e.target + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "obi2")
        elif cmd == "ERROR":
            self.state.error = e
        return e

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        self._connected.wait()
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username or "botd", server, server, self.cfg.realname or "botd"))

    def output(self):
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if txt:
                if self.sleep:
                    if (time.time() - self.state.last) < 3.0:
                        time.sleep(1.0 * (self.state.nrsend % 10))
                self._say(channel, txt, type)

    def raw(self, txt):
        txt = txt.rstrip()
        logging.info(txt)
        if self._stopped:
            return
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        self._sock.send(txt)
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt, mtype="chat"):
        if (time.time() - self.state.last) < 3.0:
            time.sleep(self.cfg.sleep * (self.state.nrsend % 10))
        self._outqueue.put((channel, txt, mtype))

    def start(self):
        if not self.cfg.server:
            return
        if self.cfg.channel:
            self.channels.append(self.cfg.channel)
        self.register(errored)
        self.register(privmsged)
        self.register(noticed)
        self.connect()
        super().start(True, True, True)

class DCC(Bot):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def raw(self, txt):
        self._fsock.write(txt.rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        self.raw(txt)

    def connect(self, event):
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.send(bytes('Welcome to BOTD %s !!\n' % event.nick, "utf-8"))
        s.setblocking(True)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.origin = event.origin
        self._connected.set()
        self.start()

    def poll(self):
        self._connected.wait()
        e = DEvent()
        e.txt = self._fsock.readline()
        e.txt = e.txt.rstrip()
        e._sock = self._sock
        e._fsock = self._fsock
        e.channel = self.origin
        e.orig = repr(self)
        e.origin = self.origin or "root@dcc"
        self.handle(e)
        return e

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        super().start(False, True, False)

def errored(handler, event):
    if event.command != "ERROR":
        return
    handler.state.error = event
    handler._connected.clear()
    time.sleep(handler.state.nrconnect * handler.cfg.sleep)
    handler.connect()

def noticed(handler, event):
    if event.command != "NOTICE":
        return
    if event.txt.startswith("VERSION"):
        from __main__ import __version__
        txt = "\001VERSION %s %s - %s\001" % ("BOTD", __version__, "python3 IRC channel daemon")
        handler.command("NOTICE", event.channel, txt)

def privmsged(handler, event):
    if event.command != "PRIVMSG":
        return
    users.userhosts.set(event.nick, event.origin)
    if event.txt.startswith("DCC CHAT"):
        if not users.allowed(event.origin, "USER"):
            return
        try:
            dcc = DCC()
            dcc.encoding = "utf-8"
            launch(dcc.connect, event)
            return
        except ConnectionRefusedError:
            return
    if event.txt and event.txt[0] == handler.cc:
        if not users.allowed(event.origin, "USER"):
            logging.error("deny %s" % event.origin)
            return
        handler.put(event)
