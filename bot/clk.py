# BOTD - 24/7 channel daemon (clk.py)
#
# this file is placed in the public domain

"clock functions (clk)"

# imports

import threading
import time

from bot.obj import Object
from bot.thr import launch

# defines

def __dir__():
    return ("Repeater", "Timer")

# classes

class Timer(Object):

    "timer"

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.sleep = sleep
        self.args = args
        self.name = kwargs.get("name", "")
        self.kwargs = kwargs
        self.state = Object()
        self.timer = None

    def run(self, *args, **kwargs):
        "run"
        self.state.latest = time.time()
        launch(self.func, *self.args, **self.kwargs)

    def start(self):
        "clock"
        if not self.name:
            self.name = self.func.__func__.__qualname__
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        "stop"
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    "repeater class"

    def run(self, *args, **kwargs):
        "run repeater"
        thr = launch(self.start, **kwargs)
        super().run(*args, **kwargs)
        return thr
