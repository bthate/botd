# BOTD - python3 IRC channel daemon.
#
# clock module providing timers and repeaters 

"""
    clock module.

    clock and timer classes that can be used to periodically run jobs.

"""

import threading
import time
import typing

from botd.dbs import Db
from botd.evt import Event
from botd.obj import Cfg, Object
from botd.thr import launch
from botd.utl import get_name

# defines

def __dir__():
    return ("Repeater", "Timer", "Timers")

# classes

class Timer(Object):

    """
        one time execution of a function at x seconds from now.
    
        Timer(sleep, funcion, name="timername")
    
        sleep is the number of seconds to sleep before running the timers function.
        function is the function to run
        name can be a provided name of the timer otherwist the timer function is the name

    """

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
        """
            start the timer
        
            start the timer after x seconds of sleep.

        """
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
        """
            run the timer's funtion. 
        
            launch the funcion in it's own thread.

        """
        self.state.latest = time.time()
        launch(self.func, *self.args, **self.kwargs)

    def exit(self):
        """
            exit timer.
        
            call cancel on the running timer.

        """
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    """
        Repeater class
    
        run a function repeatedly every x seconds.

    """

    def run(self, *args, **kwargs):
        """
            run repeater
        
            run the function and launch a thread with a new timer.

        """
        self.func(*args, **kwargs)
        return launch(self.start)
