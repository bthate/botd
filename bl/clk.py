# BOTLIB - Framework to program bots.
#
# clock module providin timers and repeaters 

import threading
import time
import typing
import bl

def __dir__():
    return ("Repeater", "Timer", "Timers")

def dummy():
    if bl.cfg.verbose:
        print("yo!")

default = {
          "latest": 0,
          "starttime": 0
         }          

class Timers(bl.pst.Persist):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stopped = False
        self.cfg = bl.cfg.Cfg(default)
        self.timers = bl.obj.Object()

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
        for evt in bl.db.all("bl.clk.Timers"):
            e = bl.evt.Event()
            bl.obj.update(e, evt)
            if "done" in e and e.done:
                continue
            if "time" not in e:
                continue
            if time.time() < int(e.time):
                self.timers[e.time] = e
        return bl.launch(self.loop)

    def stop(self):
        self._stopped = True

class Timer(bl.pst.Persist):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self._func = func
        self._name = kwargs.get("name", bl.typ.get_name(func))
        self.sleep = sleep
        self.args = args
        self.kwargs = kwargs
        self.state = bl.Object()
        bl.obj.update(self.state, default)
        self.timer = None

    def start(self):
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self._name)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer._func = self._func
        timer.start()
        self.timer = timer
        return timer

    def run(self, *args, **kwargs) -> None:
        self.state.latest = time.time()
        bl.launch(self._func, *args, **kwargs)

    def exit(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        self._func(*args, **kwargs)
        return bl.launch(self.start)
