# BOTLIB - the bot library
#
#

from .obj import Object, Default

class Token(Object):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

class Getter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
        
class Setter(Object):

    def __init__(self, txt):
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
                    
class Parsed(Default):

    def parse(self, txt):
        if not txt:
            return
        self.txt = txt
        self.args = []
        self.gets = Default()
        self.sets = Default()
        tokens = [Token(txt) for txt in txt.split()]
        for token in tokens:
            g = Getter(token.txt)
            if g:
                self.gets.update(g)
                continue
            s = Setter(token.txt)
            if s:
                self.sets.update(s)
                continue
            self.args.append(token.txt)
        self.txt =  " ".join(self.args)
        self.cmd = self.args[0]
        self.args = self.args[1:]
        self.rest = " ".join(self.args)
