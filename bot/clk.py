" clock functions (clk)"

import threading, time

from obj import Object, get_type
from thr import launch

class Timer(Object):

    "timer class"

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
        "run the timer"
        self.state.latest = time.time()
        launch(self.func, *self.args, **self.kwargs)

    def start(self):
        "start clock for timer"
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
        "stop timer"
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    "repeater class"

    def run(self, *args, **kwargs):
        "run a repeater"
        thr = launch(self.start, **kwargs)
        super().run(*args, **kwargs)
        return thr
