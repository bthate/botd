# BOTLIB - Framework to program bots.
#
# udp input to irc channel.

import bl
import socket
import time

from bl.dbs import Db
from bl.pst import Cfg, Persist
from bl.flt import Fleet
from bl.thr import launch
from bl.utl import get_name

def __dir__():
    return ("UDP", "Cfg", "init") 

fleet = Fleet()
db = Db()

def init(cfg):
    server = UDP()
    server.start()
    return server

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500
        self.password = "boh"
        self.seed = "blablablablablaz" # needs to be 16 chars wide
        self.server = self.host
        self.owner = ""

class UDP(Persist):

    def __init__(self):
        super().__init__()
        self._stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()
        
    def output(self, txt, addr=None):
        if not self.verbose:
            return
        try:
            (passwd, text) = txt.split(" ", 1)
        except ValueError:
            return
        text = text.replace("\00", "")
        if passwd == self.cfg.password:
            for b in fleet.bots:
                if "DCC" in get_name(b):
                    b.announce(text)

    def server(self, host="", port=""):
        c = self.cfg
        try:
            self._sock.bind((host or c.host, port or c.port))
        except socket.gaierror as ex:
            logging.error("EBIND %s" % ex)
            return
        while not self._stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self._stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        self._stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("bla", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        self.cfg = db.last("bl.udp.Cfg") or Cfg()
        launch(self.server)
