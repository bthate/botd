# BOTD - IRC channel daemon
#
# dispatch tables.

""" tables for load ondemand, type checking and more. """

#:
classes = {
    "Bot": "botd.bot.Bot",
    "Cfg": "botd.bot.Cfg",
    "Command": "botd.prs.Command",
    "Console": "botd.csl.Console",
    "DCC": "botd.irc.DCC",
    "DEvent": "botd.irc.DEvent",
    "Db": "botd.dbs.Db",
    "Default": "botd.obj.Default",
    "Event": "botd.evt.Event",
    "Feed": "botd.rss.Feed",
    "Fetcher": "botd.rss.Fetcher",
    "Fleet": "botd.flt.Fleet",
    "Handler": "botd.hdl.Handler",
    "IRC": "botd.irc.IRC",
    "Kernel": "botd.krn.Kernel",
    "Kernels": "botd.krn.Kernels",
    "Loader": "botd.ldr.Loader",
    "Log": "botd.ent.Log",
    "Object": "botd.dft.Object",
    "Repeater": "botd.clk.Repeater",
    "Rss": "botd.rss.Rss",
    "Seen": "botd.rss.Seen",
    "Timer": "botd.clk.Timer",
    "Todo": "botd.ent.Todo",
    "Token": "botd.prs.Token",
    "UDP": "botd.udp.UDP",
    "User": "botd.usr.User",
    "Users": "botd.usr.Users"
}

#:
modules = {
    "cfg": "botd.cfg",
    "cmds": "botd.cmd",
    "delete": "botd.rss",
    "display": "botd.rss",
    "feed": "botd.rss",
    "fetch": "botd.rss",
    "find": "botd.fnd",
    "flt": "botd.shw",
    "log": "botd.ent",
    "meet": "botd.usr",
    "pid": "botd.shw",
    "ps": "botd.shw",
    "rss": "botd.rss",
    "todo": "botd.ent",
    "up": "botd.shw",
    "users": "botd.usr",
    "v": "botd.shw"
}

#:
names = {
    "bot": "botd.bot.Bot",
    "cfg": "botd.bot.Cfg",
    "command": "botd.prs.Command",
    "console": "botd.csl.Console",
    "db": "botd.dbs.Db",
    "dcc": "botd.irc.DCC",
    "default": "botd.obj.Default",
    "devent": "botd.irc.DEvent",
    "event": "botd.evt.Event",
    "feed": "botd.rss.Feed",
    "fetcher": "botd.rss.Fetcher",
    "fleet": "botd.flt.Fleet",
    "handler": "botd.hdl.Handler",
    "irc": "botd.irc.IRC",
    "kernel": "botd.krn.Kernel",
    "kernels": "botd.krn.Kernels",
    "loader": "botd.ldr.Loader",
    "log": "botd.ent.Log",
    "object": "botd.dft.Object",
    "repeater": "botd.clk.Repeater",
    "rss": "botd.rss.Rss",
    "seen": "botd.rss.Seen",
    "timer": "botd.clk.Timer",
    "todo": "botd.ent.Todo",
    "token": "botd.prs.Token",
    "udp": "botd.udp.UDP",
    "user": "botd.usr.User",
    "users": "botd.usr.Users"
}
