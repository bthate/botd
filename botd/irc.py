# BOTD - python3 IRC channel daemon.
#
# IRC bot. 

"""
    irc class.
    
    provides an IRC bot.
    
"""


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

from botd.bot import Bot
from botd.dft import defaults
from botd.err import EINIT
from botd.evt import Event
from botd.flt import Fleet
from botd.krn import kernels
from botd.obj import Cfg, Object
from botd.thr import launch
from botd.usr import Users
from botd.utl import locked

# defines

def __dir__():
    return ('Cfg', 'DCC', 'DEvent', 'Event', 'IRC', 'init')

def init(k):
    """
        init function.
        
        starts an IRC bot and returns it.
        
    """
    bot = IRC()
    bot.cfg.last()
    bot.start()
    return bot

saylock = _thread.allocate_lock()

# classes

class Cfg(Cfg):

    """
        Cfg class.
        
        IRC configuration.
        
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(defaults.irc)

class Event(Event):

    """
        Event class
        
        basic IRC event, dispatches on command attribute (event.command)
        
    """

    def __init__(self):
        super().__init__()
        self.arguments = []
        self.channel = ""
        self.command = ""
        self.nick = ""
        self.origin = ""
        self.target = ""

class DEvent(Event):

    """
        DEvent class
        
        DCC event class, write to the DCC socket.
        
    """

    def __init__(self):
        super().__init__()
        self._sock = None
        self._fsock = None
        self.channel = ""

class TextWrap(textwrap.TextWrapper):

    """
        TextWrap class.
        
        wrap text within the IRC limited message length (480 chars long).

    """
    
    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 480

class IRC(Bot):

    """
        IRC class
        
        implements the IRC bot.
        
    """

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self._threaded = False
        self.cc = "!"
        self.cfg = Cfg()
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
        self.register("ERROR", ERROR)
        self.register("NOTICE", NOTICE)
        self.register("PRIVMSG", PRIVMSG)

    def _connect(self):
        """
            _connect method
            
            internal connecting function, used in the connect loop (with retries).

        """
        if self.cfg.ipv6:
            oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(1)
        oldsock.settimeout(5.0)
        logging.warn("connect %s:%s" % (self.cfg.server, self.cfg.port or 6667))
        oldsock.connect((self.cfg.server, int(self.cfg.port or 6667)))
        oldsock.setblocking(1)
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
        """
            _parsing method.
            
            parse text into an IRC evemt.
            
        """
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.orig = repr(self)
        o.txt = rawstr
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
                o.etype = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    @locked(saylock)
    def _say(self, channel, txt, mtype="chat"):
        """
            _say method.
            
            echo text to a channel with 3 seconds interval
            
        """
        wrapper = TextWrap()
        txt = txt.replace("\n", "")
        for t in wrapper.wrap(txt):
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 3.0:
                time.sleep(3.0)
            self.state.last = time.time()

    def _some(self, use_ssl=False, encoding="utf-8"):
        """
            _some method.
            
            wait on the IRC connection for "some" data to arrive.
            used to fill a buffer of incoming data.
            
        """
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
        """
            announce method.
            
            annouce text on joined channels.

        """
        for channel in self.channels:
            self._say(channel, txt)

    def command(self, cmd, *args):
        """
            command method
            
            generic command handler, handles basic commands.
            
        """
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
        """
            connect method.
            
            run a loop until a connection is made.
            
        """
        nr = 0
        while 1:
            self.state.nrconnect += 1
            logging.warning("connect #%s" % self.state.nrconnect)
            if self._connect():
                break
            time.sleep(nr * 3.0)
            nr += 1
        self.logon(self.cfg.server, self.cfg.nick)

    def dispatch(self, event):
        """
            dispatch method.
            
            dispatch the event based on the event.command attribute.

        """
        event._func = getattr(self, event.command, None)
        if event._func:
            event._func(event)
        event.ready()

    def poll(self):
        """
            poll method.
            
            poll on the IRC line to receive text and convert that to a received event.

        """
        self._connected.wait()
        if not self._buffer:
            try:
                self._some()
            except (ConnectionResetError, socket.timeout) as ex:
                e = Event()
                e._error = str(ex)
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
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "botd")
        elif cmd == "ERROR":
            self.state.error = e
        return e

    def joinall(self):
        """
           joinall method.
           
           join all channels in the self.channels list.
           
        """ 
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        """
            logon method
            
            echo login data to the server.
            
        """
        self._connected.wait()
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username or "botd", server, server, self.cfg.realname or "botd"))

    def output(self):
        """
            output method.
            
            loop to implement bufferd output.
            
        """
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if txt:
                self._say(channel, txt, type)

    def raw(self, txt):
        """
            raw method
            
            echo raw text on the connection.
            
        """
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
        """
            say method.
            
            put channel,txt to the output loop.
            
        """
        self._outqueue.put_nowait((channel, txt, mtype))

    def start(self):
        """
            start method.
            
            start the IRC bot and let it connect to the server.
            
        """
        k = kernels.get_first()
        k.fleet.add(self)
        if self.cfg.channel:
            self.channels.append(self.cfg.channel)
        self.connect()
        super().start(True, True)

class DCC(Bot):

    """
        DCC class
        
        implements a direct client to client bot.
        
    """

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def raw(self, txt):
        """
            raw method
            
            echo text on the DCC socket.
            
        """
        self._fsock.write(txt.rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        """
            announce method.
            
            just echo's text on the DCC socket.

        """
        self.raw(txt)

    def connect(self, event):
        """
            connect method.
            
            make a DCC socket connection.
            
        """
        k = kernels.get_first()
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((addr, port))
        except ConnectionRefusedError:
            logging.error("connection to %s:%s refused" % (addr, port))
            return
        s.send(bytes('Welcome to %s %s !!\n' % (k.cfg.name, event.nick), "utf-8"))
        s.setblocking(1)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.origin = event.origin
        self._connected.set()
        super().start(True)

    def poll(self):
        """
            poll method
            
            return an DCC event from text typed in a DCC chat session.
            
        """
        self._connected.wait()
        k = kernels.get_first()
        e = DEvent()
        e.txt = self._fsock.readline()
        e.txt = e.txt.rstrip()
        try:
            e.args = e.txt.split()[1:]
        except ValueError:
            e.args = []
        e._sock = self._sock
        e._fsock = self._fsock
        e.etype = "command"
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        k.put(e)
        return e

    def say(self, channel, txt, type="chat"):
        """
            say method
            
            echo's to the DCC socket.
            
        """
        self.raw(txt)


def ERROR(handler, event):
    """
        error handler.
        
        callback to handle errors.
        
    """
    handler.state.error = event
    handler._connected.clear()
    time.sleep(handler.state.nrconnect * 3.0)
    launch(handler.connect)

def NOTICE(handler, event):
    """
        notice handler.
        
        respond to notice queries.
        
    """
    if event.txt.startswith("VERSION"):
        txt = "\001VERSION %s %s - %s\001" % ("BOTD", "1", "python3 IRC channel daemon")
        handler.command("NOTICE", event.channel, txt)

def PRIVMSG(handler, event):
    """
        privmsg handler.
        
        read text written in a channel, check for commands and if so send to kernel for processing.
        
    """
    k = kernels.get_first()
    k.users.userhosts.set(event.nick, event.origin)
    if event.txt.startswith("DCC CHAT"):
        if not k.users.allowed(event.origin, "USER"):
            return
        try:
            dcc = DCC()
            dcc.encoding = "utf-8"
            launch(dcc.connect, event)
            return
        except ConnectionRefusedError:
            return
    if event.txt and event.txt[0] == handler.cc:
        if not k.users.allowed(event.origin, "USER"):
            return
        e = Event()
        e.etype = "command"
        e.channel = event.channel
        e.orig = repr(handler)
        e.origin = event.origin
        e.txt = event.txt.strip()[1:]
        k.put(e)
