# BOTD - python3 IRC channel daemon
#
# dispatch tables.

classes = ['bl.Cfg', 'bl.Default', 'bl.Object', 'bl.Register', 'bl.bot.Bot', 'bl.bot.Cfg', 'bl.clk.Repeater', 'bl.clk.Timer', 'bl.clk.Timers', 'bl.csl.Console', 'bl.dbs.Db', 'bl.evt.Command', 'bl.evt.Event', 'bl.evt.Token', 'bl.flt.Fleet', 'bl.hdl.Handler', 'bl.krn.Cfg', 'bl.krn.Event', 'bl.krn.Kernel', 'bl.ldr.Loader', 'bl.usr.User', 'bl.usr.Users', 'botd.ent.Log', 'botd.ent.Todo', 'botd.irc.Cfg', 'botd.irc.DCC', 'botd.irc.DEvent', 'botd.irc.Event', 'botd.irc.IRC', 'botd.rss.Cfg', 'botd.rss.Feed', 'botd.rss.Fetcher', 'botd.rss.Rss', 'botd.rss.Seen', 'botd.udp.Cfg', 'botd.udp.UDP']
names = {'cfg': 'botd.udp.Cfg', 'default': 'bl.Default', 'object': 'bl.Object', 'register': 'bl.Register', 'bot': 'bl.bot.Bot', 'repeater': 'bl.clk.Repeater', 'timer': 'bl.clk.Timer', 'timers': 'bl.clk.Timers', 'console': 'bl.csl.Console', 'db': 'bl.dbs.Db', 'command': 'bl.evt.Command', 'event': 'botd.irc.Event', 'token': 'bl.evt.Token', 'fleet': 'bl.flt.Fleet', 'handler': 'bl.hdl.Handler', 'kernel': 'bl.krn.Kernel', 'loader': 'bl.ldr.Loader', 'user': 'bl.usr.User', 'users': 'bl.usr.Users', 'log': 'botd.ent.Log', 'todo': 'botd.ent.Todo', 'dcc': 'botd.irc.DCC', 'devent': 'botd.irc.DEvent', 'irc': 'botd.irc.IRC', 'feed': 'botd.rss.Feed', 'fetcher': 'botd.rss.Fetcher', 'rss': 'botd.rss.Rss', 'seen': 'botd.rss.Seen', 'udp': 'botd.udp.UDP'}
modules = {'cfg': 'botd.cmd', 'cmds': 'botd.cmd', 'ed': 'botd.cmd', 'fleet': 'botd.cmd', 'ls': 'botd.cmd', 'meet': 'botd.cmd', 'pid': 'botd.cmd', 'ps': 'botd.cmd', 'u': 'botd.cmd', 'up': 'botd.cmd', 'v': 'botd.cmd', 'log': 'botd.ent', 'todo': 'botd.ent', 'delete': 'botd.rss', 'display': 'botd.rss', 'feed': 'botd.rss', 'fetch': 'botd.rss', 'rss': 'botd.rss'}
