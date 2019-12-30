# BOTD - python3 IRC channel daemon.
#
# clock module providing timers and repeaters 

import threading
import time
import typing

from bl import Cfg, Object
from bl.dbs import Db
from bl.evt import Event
from bl.thr import launch
from bl.utl import get_name

def __dir__():
    return ("Repeater", "Timer", "Timers")

db = Db()

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.latest =  0
        self.starttime =  0

def echo():
    print("yo!")

class Timers(Object):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._stopped = False
        self.cfg = Cfg()
        self.timers = Object()

    def loop(self):
        while not self._stopped:
            time.sleep(1.0)
            remove = []
            for t in self.timers:
                event = self.timers[t]
                if time.time() > t:
                    self.cfg.latest = time.time()
                    self.cfg.save()
                    event.raw(event.txt)
                    remove.append(t)
            for r in remove:
                del self.timers[r]

    def start(self):
        for evt in db.all("bl.clk.Timers"):
            e = Event()
            e.updateevt)
            if "done" in e and e.done:
                continue
            if "time" not in e:
                continue
            if time.time() < int(e.time):
                self.timers[e.time] = e
        return launch(self.loop)

    def stop(self):
        self._stopped = True

class Timer(Object):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._func = None
        self.sleep = None
        self.args = args
        self.kwargs = kwargs
        self.state = Object()
        self.timer = None

    def start(self, func=echo, sleep=300.0, name=""):
        if not name:
            name = get_name(self._func))
        self._name = name
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self._name)
        timer.sleep = sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer._func = func
        timer.start()
        self.timer = timer
        return timer

    def run(self, *args, **kwargs) -> None:
        self.state.latest = time.time()
        launch(self._func, *args, **kwargs)

    def exit(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        self._func(*args, **kwargs)
        return launch(self.start)
