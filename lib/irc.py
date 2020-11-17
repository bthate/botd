"Internet Relay Chat"

import os, queue, socket, textwrap, time, threading, _thread

from bus import bus
from dbs import find, last
from hdl import Event, Handler
from obj import Cfg, Default, Object, register, save, update
from ofn import format
from prs import parse, parse_cli
from thr import launch

__version__ = 109

saylock = _thread.allocate_lock()

def init(hdl):
    "create a IRC bot and return it"
    i = IRC()
    i.clone(hdl)
    return launch(i.start)

def locked(l):
    "lock descriptor"
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockeddec.__doc__ = func.__doc__
        return lockedfunc
    return lockeddec

class ENOUSER(Exception):

    "no matching user found"

class Cfg(Cfg):

    "IRC configuration object"

    def __init__(self):
        super().__init__()
        self.channel = "#bot"
        self.nick = "bot"
        self.server = "localhost"
        self.username = "bot"
        self.realname = "bot"
                 
class Event(Event):

    "IRC event"

    def show(self):
        for txt in self.result:
            self.src.say(self.channel, txt)
    
class TextWrap(textwrap.TextWrapper):

    "text wrapper"

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450

class IRC(Handler):

    "IRC bot"

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._joined = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._trc = ""
        self.cc = "!"
        self.cfg = Cfg()
        self.cmds = Object()
        self.channels = []
        self.speed = "slow"
        self.state = Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.verbose = False
        register(self.cmds, "ERROR", self.ERROR)
        register(self.cmds, "LOG", self.LOG)
        register(self.cmds, "NOTICE", self.NOTICE)
        register(self.cmds, "PRIVMSG", self.PRIVMSG)
        register(self.cmds, "QUIT", self.QUIT)
        register(self.cmds, "366", self.JOINED)
        bus.add(self)
 
    def _connect(self, server):
        "connect (blocking) to irc server"
        oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(1)
        oldsock.settimeout(5.0)
        try:
            oldsock.connect((server, 6667))
        except (OSError, ConnectionError):
            time.sleep(2.0)
            try:
                oldsock.connect((server, 6667))
            except (OSError, ConnectionError):
                self._connected.set()
                return False
        oldsock.setblocking(1)
        oldsock.settimeout(1200.0)
        self._sock = oldsock
        self._fsock = self._sock.makefile("r")
        fileno = self._sock.fileno()
        os.set_inheritable(fileno, os.O_RDWR)
        self._connected.set()
        return True

    def _parsing(self, txt):
        "parse incoming text into an event"
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.rawstr = rawstr
        o.orig = repr(self)
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
                o.type = o.command
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
    def _say(self, channel, txt):
        "say something on a channel"
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            if not t:
                continue
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def _some(self):
        "blocking read on the socket"
        inbytes = self._sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        "annouce text on all channels"
        for channel in self.channels:
            self.say(channel, txt)

    def command(self, cmd, *args):
        "send a command to the irc server"
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

    def connect(self, server, nick):
        "connect to server and identify with nick"
        nr = 0
        while not self.stopped:
            self.state.nrconnect += 1
            if self._connect(server):
                break
            time.sleep(10.0)
            nr += 1
        self._connected.wait()
        self.logon(server, nick)

    def handle(self, event):
        if event.command in self.cmds:
            self.cmds[event.command](event)

    def doconnect(self):
        "start input/output tasks on connect"
        assert self.cfg.server
        assert self.cfg.nick
        super().start()
        self.connect(self.cfg.server, self.cfg.nick)
        launch(self.input)
        launch(self.output)

    def input(self):
        "loop for input"
        while not self.stopped:
            try:
                e = self.poll()
            except (OSError, ConnectionResetError, socket.timeout) as ex:
                e = Event()
                e.error = str(ex)
                self.ERROR(e)
                break
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            self.handle(e)

    def joinall(self):
        "join all channels"
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        "do logon handshake"
        self._connected.wait()
        assert self.cfg.username
        assert self.cfg.realname
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname))

    def output(self):
        "loop for output"
        while 1:
            channel, txt = self._outqueue.get()
            if channel is None:
                break
            if txt:
                time.sleep(0.001)
                self._say(channel, txt)

    def poll(self):
        "block on socket and do basic response"
        self._connected.wait()
        if not self._buffer:
            self._some()
        if not self._buffer:
            return self._parsing("")
        e = self._parsing(self._buffer.pop(0))
        cmd = e.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "366":
            self._joined.set()
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "botd")
        return e

    def raw(self, txt):
        "send text on raw socket"
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        self._connected.wait()
        try:
            self._sock.send(txt)
        except (OSError, ConnectionResetError) as ex:
            e = Event()
            e.error = str(ex)
            self.LOG(e)
            self._connected.clear()
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt):
        "forward to output loop"
        self._outqueue.put_nowait((channel, txt))

    def start(self, cfg=None):
        "start the irc bot"
        if cfg is not None:
            self.cfg.update(cfg)
        else:
            last(self.cfg)
        assert self.cfg.channel
        assert self.cfg.server
        self.channels.append(self.cfg.channel)
        self._joined.clear()
        launch(self.doconnect)
        self._joined.wait()

    def stop(self):
        "stop the irc bot"
        super().stop()
        self._outqueue.put((None, None))
        try:
            self._sock.shutdown(2)
        except OSError:
            pass

    def ERROR(self, event):
        "error handling"
        self.state.nrerror += 1
        self.state.error = event.error
        self._connected.clear()
        self.stop()
        self.start()

    def JOINED(self, event):
        "joined all channels"
        self._joined.set()

    def LOG(self, event):
        "log to console"
        if self.verbose:
            print(event)

    def NOTICE(self, event):
        "handle noticed"
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % ("OBJ", obj.__version__, "object programming library")
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, event):
        "handle a private message"
        if event.txt.startswith("DCC CHAT"):
            if self.cfg.users and not users.allowed(event.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.encoding = "utf-8"
                dcc.clone(self)
                launch(dcc.connect, event)
                return
            except ConnectionError as ex:
                print(ex)
                return
        if event.txt and event.txt[0] == self.cc:
            if self.cfg.users and not users.allowed(event.origin, "USER"):
                return
            event.txt = event.txt[1:]
            event.iscmd = True
            self.put(event)

    def QUIT(self, event):
        "handle quit"
        if self.cfg.server in event.orig:
            self.stop()

class DCC(Handler):

    "direct client to client"

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def raw(self, txt):
        "send text on the dcc socket"
        self._fsock.write(str(txt).rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        "overload if needed"

    def connect(self, event):
        "connect to the offering socket"
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.setblocking(1)
        #os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.raw('Welcome %s' % event.nick)
        self.origin = event.origin
        launch(self.input)
        super().start()
        self._connected.set()

    def input(self):
        "loop for input"
        while 1:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def poll(self):
        "poll (blocking) for input and create an event for it"
        self._connected.wait()
        e = Event()
        txt = self._fsock.readline()
        txt = txt.rstrip()
        parse(e, txt)
        e._sock = self._sock
        e._fsock = self._fsock
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        return e

    def say(self, channel, txt):
        "skip channel and print on socket"
        self.raw(txt)

class User(Object):

    "IRC user"

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Object):

    "IRC users"

    userhosts = Object()

    def allowed(self, origin, perm):
        "see if origin has needed permission"
        perm = perm.upper()
        origin = get(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        "remove a permission of the user"
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        "get all users, optionaly provding an matching origin"
        s = {"user": origin}
        return find("irc.User", s)

    def get_user(self, origin):
        "get specific user with corresponding origin"
        u = list(self.get_users(origin))
        if u:
            return u[-1][-1]

    def meet(self, origin, perms=None):
        "add a irc user"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        "grant origin oper permission"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        "add permission to origin"
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user

users = Users()

def cfg(event):
    "configure irc."
    c = Cfg()
    last(c)
    if not event.prs.sets:
        return event.reply(format(c, skip=["username", "realname"]))
    update(c, event.prs.sets)
    save(c)
    event.reply("ok")
