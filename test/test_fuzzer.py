"call all methods"

import os, sys ; sys.path.insert(0, os.getcwd())

import inspect
import types
import unittest
import bot.obj
import bot.cmd

from bot.obj import Object, get
from bot.hdl import Event, Handler, mods
from bot.prs import parse_cli
from bot.thr import get_exception

def cb(event):
    print("yoo")

cfg = parse_cli()
debug = "d" in cfg.opts
exclude = ["poll", "handler", "input", "doconnect", "raw", "start"]
exc = []
result = []
verbose = "v" in cfg.opts

values = Object()
values["txt"] = "yoo"
values["key"] = "txt"
values["value"] = Object()
values["d"] = {}
values["hdl"] = Handler()
values["event"] = Event({"txt": "thr", "error": "test"})
values["path"] = bot.obj.wd
values["channel"] = "#bot"
values["orig"] = repr(values["hdl"])
values["obj"] = Object()
values["d"] = {}
values["value"] = 1
values["pkgnames"] = "bot"
values["name"] = "bot"
values["callback"] = cb
values["e"] = Event()
values["mod"] = bot.cmd
values["mns"] = "irc,udp,rss"
values["sleep"] = 60.0
values["func"] = cb
values["origin"] = "test@shell"
values["perm"] = "USER"
values["permission"] = "USER"
values["text"] = "yoo"
values["server"] = "localhost"
values["nick"] = "bot"
values["rssobj"] = Object()
values["o"] = Object()

def get_values(vars):
    args = []
    for k in vars:    
       res = get(values, k, None)
       if res:
           args.append(res)
    return args

def handle_type(ex):
    if debug and verbose:
        print(ex)

def fuzz(mod, *args, **kwargs):
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if "_" in name:
            continue
        try:
            oo = o()
        except TypeError as ex:
            handle_type(ex)
            continue
        for name, meth in inspect.getmembers(oo):
            if "_" in name or name in exclude:
                continue
            try:
                spec = inspect.getfullargspec(meth)
                args = get_values(spec.args[1:])
            except TypeError as ex:
                handle_type(ex)
                continue
            if debug and verbose:
                print(meth)
            try:
                res = meth(*args, **kwargs)
                if debug:
                    print("%s(%s) -> %s" % (name, ",".join(args), res))
            except Exception as ex:
                if debug:
                    print(get_exception())
        
class Test_Fuzzer(unittest.TestCase):

    def test_fuzz(self):
        global exc
        m = mods("bot")
        for x in range(cfg.index or 1):
            for mod in m:
                fuzz(mod)
        exc = []
