# BOTD - IRC channel daemon.
#
# clock module providing timers and repeaters 

import threading
import time
import typing

from botd.dbs import Db
from botd.evt import Event
from botd.obj import Cfg, Object
from botd.thr import launch
from botd.utl import get_name

def __dir__():
    return ("Repeater", "Timer", "Timers")

class Timer(Object):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.sleep = sleep
        self.args = args
        self.name = kwargs.get("name", "")
        self.kwargs = kwargs
        self.state = Object()
        self.timer = None

    def start(self):
        if not self.name:
            self.name = get_name(self.func)
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self.name)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def run(self, *args, **kwargs):
        self.state.latest = time.time()
        launch(self.func, *self.args, **self.kwargs)

    def exit(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        thr = launch(self.start)
        self.func(*args, **kwargs)
        return thr
