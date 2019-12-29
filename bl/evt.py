# BOTD - python3 IRC channel daemon.
#
# Event base class and command parsing

import time
import threading

from bl.err import ENOTIMPLEMENTED, ENOTXT
from bl.gnr import format
from bl.obj import Object
from bl.hdl import Handler
from bl.pst import Persist
from bl.tbl import names
from bl.tms import parse_date, to_day

def __dir__():
    return ("Command", "Event", "Object", "Token", "aliases")

aliases = {}
h = Handler()

class Token(Object):

    def __init__(self):
        super().__init__()
        self.arg = ""
        self.chk = ""
        self.dkey = ""
        self.down = None
        self.index = None
        self.ignore = ""
        self.match = ""
        self.noignore = False
        self.option = ""
        self.selector = ""
        self.setter = ""
        self.value = ""
        self.up = None

    def parse(self, nr, word):
        if nr == 0:
            if word.startswith("!"):
                word = word[1:]
            if word:
                self.chk = word
            return
        if word.startswith("-"):
            try:
                self.down = word
            except ValueError:
                pass
            self.option += word[1:]
            self.value = self.option
            return
        try:
            self.index = int(word)
            #self.arg = word
            return
        except ValueError:
            pass
        if nr == 1:
            self.match = names.get(word, word)
            self.arg = word
            return
        if "http" in word:
            self.value = word
            self.arg = word
            return
        if word.startswith("+"):
            try:
                self.up = int(word[1:])
                return
            except ValueError:
                pass
        if word.endswith("+"):
            self.noignore = True
        if word.endswith("-"):
            word = word[:-1]
            self.ignore = word
        if "==" in word:
            self.selector, self.value = word.split("==")
            self.dkey = self.selector
        elif "=" in word:
            self.setter, self.value = word.split("=")
            self.dkey = self.setter
        else:
            self.arg = word
            self.dkey = word
            self.value = word
        if nr == 2 and not self.selector and not self.setter:
            self.selector = word
            self.value = None

class Command(Persist):

    def __init__(self):
        super().__init__()
        self._cb = None
        self._error = None
        self._func = None
        self._parsed = False
        self._ready = threading.Event()
        self._thrs = []
        self.args = []
        self.cc = ""
        self.delta = 0
        self.dkeys = []
        self.index = None
        self.match = None
        self.noignore = ""
        self.options = ""
        self.orig = ""
        self.origin = ""
        self.rest = ""
        self.result = []
        self.selector = {}
        self.setter = {}
        self.start = None
        self.stop = None
        self.time = 0
        self.txt = ""

    def aliased(self, txt):
        global aliases
        spl = txt.split()
        if spl and spl[0] in aliases:
            cmd = spl[0]
            v = aliases.get(cmd, None)
            if v:
                spl[0] = v
        return " ".join(spl)

    def parse(self, txt="", options=""):
        if not txt:
            txt = self.txt 
        if not txt:
            raise ENOTXT
        self.txt = txt
        txt = txt.replace("\u0001", "")
        txt = txt.replace("\001", "")
        if txt and self.cc == txt[0]:
            txt = txt[1:]
        txt = self.aliased(txt)
        nr = -1
        self.args = []
        self.dkeys = []
        self.options = options or self.options
        words = txt.split()
        tokens = []
        nr = -1
        for word in words:
            nr += 1
            token = Token()
            token.parse(nr, word)
            tokens.append(token)
        nr = -1
        prev = ""
        for token in tokens:
            nr += 1
            if prev:
                self.options += token.value
                continue
            if token.chk:
                self.chk = token.chk
            if token.match:
                self.match = token.match
            if token.index:
                self.index = token.index
                self.args.append(token.arg)
            if token.option:
                self.options += "," + token.option
            if prev == "-o":
                prev = ""
                self.options += "," + token.value
            if token.down:
                prev = token.down
            if token.noignore:
                self.noignore = token.noignore
            if token.selector:
                self.selector[token.selector] = token.value
            if token.setter:
                self.setter[token.setter] = token.value
            if token.up:
                self.delta = parse_date(token.up)
            elif token.down:
                self.delta = parse_date(token.down)
            if not self.noignore and token.ignore:
                self.ignore = token.ignore
                continue
            if token.dkey and not token.dkey in self.dkeys:
                self.dkeys.append(token.dkey)
            if token.arg:
                self.args.append(token.arg)
        for opt in self.options.split(","):
            try:
                self.index = int(opt)
                break
            except ValueError:
                pass
        self.start = time.time() + self.delta
        self.stop = time.time()
        self.rest = " ".join(self.args)
        self.time = to_day(self.rest)

    def ready(self):
        self._ready.set()
        
    def wait(self):
        self._ready.wait()
        thrs = []
        vals = []
        for thr in self._thrs:
            thr.join()
            thrs.append(thr)
        for thr in thrs[::-1]:
            self._thrs.remove(thr)
        self.ready()
        return self

class Event(Command):

    def __init__(self, txt=""):
        super().__init__()
        self._calledfrom = None
        self.channel = ""
        self.chk = ""
        self.dolog = False
        self.type = "chat"
        self.name = ""
        self.sep = "\n"
        self.txt = txt
        if self.txt:
            self.chk = self.txt.split()[0]
        self.verbose = True

    def display(self, o, txt=""):
        if "k" in self.options:
            self.reply("|".join(o))
            return
        if "d" in self.options:
            self.reply(str(o))
            return
        full = False
        if "f" in self.options:
            full = True
        if not full and self.dkeys:
            txt += " " + format(o, self.dkeys, full)
        else:
            txt += " " + format(o, full=full)
        if "t" in self.options:
            try: 
                txt += " %s" % bl.tms.days(o.__path__)
            except Exception as ex:
                pass
        txt = txt.strip()
        if txt:
            self.reply(txt)

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        if not self.verbose:
            return
        for txt in self.result:
            print(txt)
