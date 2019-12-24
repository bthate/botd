# BOTLIB - Framework to program bots.
#
# console code.

import sys
import bl

def __dir__():
    return ("Console",)

class Console(bl.hdl.Handler, bl.pst.Persist):

    def __init__(self):
        super().__init__()
        self.verbose = True
        
    def announce(self, txt: str) -> None:
        self.raw(txt)

    def poll(self) -> None:
        e = bl.evt.Event()
        e.options = bl.cfg.options
        e.orig = repr(self)
        e.origin = "root@shell"
        e.txt = input("> ")
        return e

    def input(self) -> None:
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            bl.k.put(e)
            e.wait()

    def raw(self, txt: str) -> None:
        if not self.verbose or not txt:
            return
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel: str, txt: str, type="chat") -> None:
        self.raw(txt)
 
    def start(self, handler=False, input=True, output=False) -> None:
        bl.fleet.add(self)
        super().start(handler, input, output)
