# BOTD - 24/7 channel daemon (tbl.py)
#
# this file is placed in the public domain

"tables (tbl)"

from bot.obj import Object, Ol, update

#:
modnames = Object()

#:
names = Ol()

update(modnames, {"cfg": "bot.cmd", "cmd": "bot.cmd", "dne": "bot.cmd", "dpl": "bot.cmd", "flt": "bot.cmd", "fnd": "bot.cmd", "ftc": "bot.cmd", "log": "bot.cmd", "rem": "bot.cmd", "rss": "bot.cmd", "tdo": "bot.cmd", "thr": "bot.cmd", "ver": "bot.cmd"})

update(names, {"bus": ["bot.hdl.Bus"], "cfg": ["bot.udp.Cfg", "bot.obj.Cfg", "bot.irc.Cfg", "bot.rss.Cfg"], "command": ["bot.hdl.Command"], "dcc": ["bot.irc.DCC"], "default": ["bot.obj.Default"], "event": ["bot.irc.Event", "bot.hdl.Event"], "feed": ["bot.rss.Feed"], "fetcher": ["bot.rss.Fetcher"], "handler": ["bot.hdl.Handler"], "irc": ["bot.irc.IRC"], "log": ["bot.cmd.Log"], "object": ["bot.obj.Object"], "ol": ["bot.obj.Ol"], "repeater": ["bot.clk.Repeater"], "rss": ["bot.rss.Rss"], "timer": ["bot.clk.Timer"], "todo": ["bot.cmd.Todo"], "udp": ["bot.udp.UDP"], "user": ["bot.usr.User"], "users": ["bot.usr.Users"]})
