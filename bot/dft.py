# BOTLIB - Framework to program bots.
#
# default values.

import lo

def __dir__():
    return ("defaults", )

#:
default_irc = {
    "channel": "",
    "nick": "botlib",
    "ipv6": False,
    "port": 6667,
    "server": "",
    "ssl": False,
    "realname": "botlib",
    "username": "botlib"
}

#:
default_krn = {
    "workdir": "",
    "kernel": False,
    "modules": "",
    "options": "",
    "prompting": True,
    "dosave": False,
    "level": "",
    "logdir": "",
    "shell": False
}

#:
default_rss = {
    "display_list": "title,link",
    "dosave": True,
    "tinyurl": False
}

defaults = lo.Object()
defaults.irc = lo.Object(default_irc)
defaults.krn = lo.Object(default_krn)
defaults.rss = lo.Object(default_rss)
