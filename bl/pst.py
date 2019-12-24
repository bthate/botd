# BOTLIB - Framework to program bots.
#
# persistence.

import bl
import bl.utl
import datetime
import json
import json.decoder
import os
import _thread

lock = _thread.allocate_lock()

class Persist(bl.Object):

    @bl.utl.locked(lock)
    def load(self, path):
        assert path
        assert bl.workdir
        lpath = os.path.join(bl.workdir, "store", path)
        if not os.path.exists(lpath):
            bl.utl.cdir(lpath)
        with open(lpath, "r") as ofile:
            try:
                val = json.load(ofile, object_hook=hooked)
            except json.decoder.JSONDecodeError as ex:
                raise bl.err.EJSON(str(ex) + " " + lpath)
            bl.update(self, val)
        self.__path__ = path
        return self

    @bl.utl.locked(lock)
    def save(self, path="", stime=None):
        assert bl.workdir
        self._type = bl.typ.get_type(self)
        if not path:
            try:
                path = self.__path__
            except AttributeError:
                pass
        if not path or stime:
            if not stime:
                stime = str(datetime.datetime.now()).replace(" ", os.sep)
            path = os.path.join(self._type, stime)
        opath = os.path.join(bl.workdir, "store", path)
        bl.utl.cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(self, ofile, default=bl.obj.default, indent=4, sort_keys=True)
        self.__path__ = path
        return path

def hooked(d):
    if "_type" in d:
        t = d["_type"]
        o = bl.typ.get_cls(t)()
    else:
        o = bl.Object()
    bl.update(o, d)
    return o
