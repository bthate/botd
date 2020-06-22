BOTD
======

Welcome to BOTD, the 24/7 channel daemon ! see https://pypi.org/project/botd/ , it's public domain ;]

BOTD can fetch RSS feeds, lets you program your own commands, can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to let
it restart after reboots. BOTD is the result of 20 years of programming bots, was there 
in 2000, is here in 2020, has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTD truely free (pastable) code you can use how you see fit, i hope you enjoy 
using and programming BOTD till the point you start programming your own bots yourself.

have fun coding ;]

I N S T A L L
=============

you can download with pip3 and install globally:

::

 > sudo pip3 install botd

You can also download the tarball and install from that, see https://pypi.org/project/botd/#files

if you want to develop on the bot clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/bthate/botd

if you want to run the bot 24/7 you can install BOTd as a service for
the systemd daemon. You can do this by running the following:

::

 > sudo bcmd install

if you don't want the bot to startup at boot, remove the service file:

::

 > sudo bcmd remove

C O N F I G
===========

to configure the bot use the ed (edit) command, with sudo:

::

 > bcmd cfg server=<server> channel=<channel> nick=<nick>
 > bcmd hup

U S A G E
=========

BOTD detects whether it is run as root or as a user. if it's root it
will use the /var/lib/botd directory and it it's user it will use ~/.bot

BOTD has it's own CLI, you can run it by giving the bot command on the
prompt, it will return with its own prompt:

::

 > bot
 > cmds
 cfg|cmds|ed|find|fleet|meet|ps|udp
 >

you can use bcmd with arguments to run a command directly:

::

 > bcmd cmds
 cfg|cmds|ed|find|fleet|meet|ps|udp

if you run with sudo, you will get additional command like ed,install,remove and hup:

::

 > sudo bcmd cmds
 cfg|cmds|ed|find|fleet|hup|install|meet|ps|remove|udp


R S S
=====

to add an url use the rss command with an url:

::

 > bcmd rss https://news.ycombinator.com/rss
 ok 1

run the rss command to see what urls are registered:

::

 > bcmd rss
 0 https://news.ycombinator.com/rss

the fetch command can be used to poll the added feeds:

::

 > bcmd fetch
 fetched 0

U D P
=====

using udp to relay text into a channel, use the okudp program to send text via the bot 
to the channel on the irc server:

::

 > tail -f /var/log/syslog | bcmd udp

to send the tail output to the IRC channel, send a udp packet to the bot:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

S O U R C E
===========

BOTD used the BOTLIB package that has the following modules.

::

    bot.clk             - clock/repeater
    bot.csl             - console
    bot.fil             - file 
    bot.hdl             - handler
    bot.irc             - internet relay chat
    bot.itr             - introspect
    bot.krn             - core handler
    bot.obj             - base classes
    bot.prs             - parse
    bot.shl             - shell
    bot.thr             - threads
    bot.tms             - time
    bot.trc             - trace


BOTD itself provides these modules:

::

    botd.cmd             - commands
    botd.opr             - opers
    botd.rss             - rich site syndicate
    botd.udp             - udp to channel

You can add you own modules to the botd package, its a namespace package.


C O N T A C T
=============

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
