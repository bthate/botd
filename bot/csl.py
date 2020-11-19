"console (csl)"

import atexit, os, pwd, readline, sys

from bot.hdl import Event, Handler
from bot.thr import launch
from bot.trm import termsave, termreset

def __dir__():
    return ("Console", "setcompleter")

cmds = []

class Event(Event):

    def direct(self, txt):
        self.src.direct(txt)

class Console(Handler):

    "console class"

    def announce(self, txt):
        "silence announcing"

    def direct(self, txt):
        "print to stdout"
        print(txt)

    def input(self):
        "loop for input"
        while 1:
            try:
                event = self.poll()
            except EOFError:
                break
            self.put(event)
            event.wait()

    def handler(self):
        super().handler()
            
    def poll(self):
        "wait for input"
        e = Event()
        e.orig = repr(self)
        e.otxt = e.txt = input("> ")
        return e

    def say(self, channel, txt):
        "strip channel from output"
        self.direct(txt)

    def start(self):
        "start console"
        super().start()
        launch(self.input)

def complete(text, state):
    "complete matches"
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def getcompleter():
    "return the completer"
    return readline.get_completer()

def setcompleter(commands):
    "set the completer"
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
