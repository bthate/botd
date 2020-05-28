# BOTLIB - Framework to program bots.
#
#

""" object editor. """

import lo
import os

from bot.dft import defaults

def __dir__():
    return ("ed",)

def ed(event):
    """ edit the last saved object of a type. """
    assert(lo.workdir)
    if not event.args:
        files = [x for x in os.listdir(os.path.join(lo.workdir, "store"))]
        if files:
            event.reply("|".join(list(files)))
        return
    cn = event.args[0]
    db = lo.Db()
    l = db.last(cn)
    if not l:     
        dft = defaults.get(cn, None)
        if dft:
            c = lo.typ.get_cls(cn)
            l = c()
            l.update(dft)
            event.reply("created %s" % cn)
        else:
            event.reply("no %s found." % cn)
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    p = l.save()
    event.reply("ok %s" % p)
