# BOTLIB - Framework to program bots.
#
#

import lo
import logging
import socket
import time

from bot import k

def __dir__():
    return ("UDP", "Cfg", "init", "toudp") 

def init(kernel):
    server = UDP()
    server.start()
    return server

class Cfg(lo.Object):

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500
        self.verbose = lo.cfg.verbose

class UDP(lo.Object):

    def __init__(self):
        super().__init__()
        self._stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()
        
    def output(self, txt, addr):
        for bot in k.fleet.bots:
            bot.announce(txt.replace("\00", ""))

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
            try:
                self.output(data, addr)
            except Exception as ex:
                logging.error(lo.trc.get_exception())

    def exit(self):
        self._stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        self.cfg.last()
        k.launch(self.server)

def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))
