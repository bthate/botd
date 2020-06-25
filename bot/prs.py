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
        nr = -1
        for token in tokens:
            nr += 1
            if self.gets.update(Getter(token.txt)):
                continue
            if self.sets.update(Setter(token.txt)):
                continue            
            if nr == 0:
                self.cmd = token.txt
            self.args.append(token.txt)
        self.txt =  " ".join(self.args)
        self.args = self.args[1:]
        self.rest = " ".join(self.args)
