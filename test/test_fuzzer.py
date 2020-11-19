"call all methods"

import os, sys ; sys.path.insert(0, os.getcwd())

import inspect
import types
import unittest
import bot.obj

from bot.obj import Object, get
from bot.hdl import Event, Handler, mods
from bot.prs import parse_cli
from bot.thr import get_exception

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

def get_values(vars):
    args = []
    for k in vars:    
       res = get(values, k, None)
       if res:
           args.append(res)
    return args

def handle_type(ex):
    if debug:
        print(ex)

def fuzz(mod, *args, **kwargs):
    
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if "__" in name:
            continue
        try:
            oo = o()
        except TypeError as ex:
            handle_type(ex)
            continue
        for name, meth in inspect.getmembers(oo):
            if "__" in name or name in exclude:
                continue
            try:
                spec = inspect.getfullargspec(meth)
                args = get_values(spec.args[1:])
            except TypeError as ex:
                handle_type(ex)
                continue
            if debug:
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
