# BOTD - python3 IRC channel daemon.
#
# default values.

from botd.obj import Object

default_irc = {
    "channel": "",
    "nick": "botd",
    "ipv6": False,
    "port": 6667,
    "server": "",
    "ssl": False,
    "realname": "python3 IRC channel daemon",
    "username": "botd"
}

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

defaults = Object()
defaults.irc = Object(default_irc)
defaults.krn = Object(default_krn)
