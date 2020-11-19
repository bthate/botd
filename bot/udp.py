"udp to irc relay"

import select, socket, sys, time

from bus import bus
from dbs import last
from obj import Cfg, Object
from thr import launch

def init(hdl):
    "start a udp to irc relay server and return it"
    u = UDP()
    return launch(u.start)

class Cfg(Cfg):

    "udp configuration"

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500

class UDP(Object):

    "udp to irc relay server"

    def __init__(self):
        super().__init__()
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def output(self, txt, addr):
        "output message on fleet"
        for bot in bus:
            bot.announce(txt.replace("\00", ""))

    def server(self):
        "loop for output"
        try:
            self._sock.bind((self.cfg.host, self.cfg.port))
        except (socket.gaierror, OSError):
            return
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        "stop udp to irc relay server"
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        "start udp to irc relay server"
        last(self.cfg)
        launch(self.server)

def toudp(host, port, txt):
    "send text over udp to the udp to irc relay server"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))

def udp(event):
    "send text over udp to the bot"
    cfg = Cfg()
    last(cfg)
    if len(sys.argv) > 2:
        txt = " ".join(sys.argv[2:])
        toudp(cfg.host, cfg.port, txt)
        return
    if not select.select([sys.stdin, ], [], [], 0.0)[0]:
        return
    while 1:
        try:
            (i, o, e) = select.select([sys.stdin,], [], [sys.stderr,])
        except KeyboardInterrupt:
            return
        if e:
            break
        stop = False
        for sock in i:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            toudp(cfg.host, cfg.port, txt)
        if stop:
            break
