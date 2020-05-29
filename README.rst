.. title:: no copyright, no LICENSE, placed in the public domain

Welcome to BOTD, an IRC channel daemon serving 24/7 in the background, see https://pypi.org/project/botd/ ;]

| 

BOTD
####

BOTD  can fetch RSS feeds, lets you program your own commands, can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to let
it restart after reboots. BOTD is the result of 20 years of programming bots, was there 
in 2000, is here in 2020, has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTD truely free (pastable) code you can use how you see fit, i hope you enjoy 
using and programming BOTD till the point you start programming your own bots yourself.

Have fun coding ;]

|

U S A G E
=========

::

 > botd --help

 usage: .

  > bot				- starts a shell
  > bot <cmd>         		- executes a command
  > bot cmds			- shows list of commands
  > bot -m <mod1,mod2>		- load modules
  > bot mods			- shows loadable modules
  > bot -w <dir>		- use directory as workdir, default is ~/.botd
  > bot cfg			- show configuration
  > bot -d			- run as daemon
  > bot -r			- root mode, use /var/lib/botd
  > bot -o <op1,op2>		- set options
  > bot -l <level>		- set loglevel

 example:

  > bot -m bot.irc -s localhost -c \#dunkbots -n botd --owner root@shell


I N S T A L L
=============

you can download with pip3 and install globally:

::

 > sudo pip3 install botd 

You can also download the tarball and install from that, see https://pypi.org/project/botd/#files

::

 > sudo python3 setup.py install

or install locally from tarball as a user:

::

 > sudo python3 setup.py install --user

if you want to develop on the bot clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botlib/botd

S E R V I C E
=============

if you want to run the bot 24/7 you can install BOTD as a service for
the systemd daemon. You can do this by running the botcfg program which let's you 
enter <server> <channel> <nick> <modules> <owner> on the command line:

::

 > sudo botcfg localhost \#botd botd bot.irc,bot.rss ~bart@127.0.0.1

botcfg installs a service file in /etc/systemd/system, installs data in /var/lib/botd and runs bothup to restart the service with the new configuration.
logs are in /var/log/botd/botd.log. If you don't want botd to start at boot, remove the botd.service file:

::

 > sudo rm /etc/systemd/system/botd.service 


U S E R S
=========

The bot only allows communication to registered users. You can add the
userhost of the owner with the --owner option:

::

 > bot --owner root@shell
 > ok

The owner of the bot is also the only one who can add other users to the
bot:

::

 > bot meet ~dunker@jsonbot/daddy
 > ok

I R C
=====

IRC (bot.irc) need the -s <server> | -c <channel> | -n <nick> | --owner <userhost> options:

::

 > bot -m bot.irc -s localhost -c \#dunkbots -n botd --owner ~bart@192.168.2.1 

for a list of modules to use see the mods command.

::

 > bot -m bot.shw mods
 bot.ed|bot.irc|bot.dft|bot.krn|bot.usr|bot.shw|bot.udp|bot.ent|bot.rss|bot.flt|bot.fnd

C O M M A N D L I N E
=====================

the basic program is called (?) bot, you can run it by tying bot on the
prompt, it will return with its own prompt:

::

 > bot
 > cmds
 cfg|cmds|fleet|mods|ps|up|v

if you provide bot with an argument it will run the bot command directly:

::

 > bot cmds
 cfg|cmds|ed|fleet|mods|ps|up|v

with the -m option you can provide a comma seperated list of modules to load:

::

 > bot -m bot.rss rss
 https://www.telegraaf.nl/rss

R S S
=====

the rss plugin uses the feedparser package, you need to install that yourself:

::

 > pip3 install feedparser

starts the rss fetcher with -m bot.rss.

to add an url use the rss command with an url:

::

 > bot rss https://news.ycombinator.com/rss
 ok 1

run the rss command to see what urls are registered:

::

 > bot rss
 0 https://news.ycombinator.com/rss

the fetch command can be used to poll the added feeds:

::

 > bot fetch
 fetched 0

U D P
=====

using udp to relay text into a channel, use the botudp program to send text via the bot 
to the channel on the irc server:

::

 > tail -f ~/.botd/logs/botd.log | botudp 

to send a message to the IRC channel, send a udp packet to the bot:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

C O D I N G
===========

.. _source:

BOTD  contains the following modules:

::

    bot			- botlib
    bot.dft             - default
    bot.ent		- log,todo
    bot.irc             - irc bot
    bot.rss             - rss to channel
    bot.udp             - udp to channel

BOTDuses the LIBOBJ library which also gets included in the package:

::

    lo			- libobj
    lo.clk              - clock
    lo.csl              - console 
    lo.flt              - fleet
    lo.ed		- editor
    lo.fnd		- search objects
    lo.gnr		- generic
    lo.hdl              - handler
    lo.krn              - core handler
    lo.shl              - shell
    lo.shw              - show runtime
    lo.thr              - threads
    lo.tms              - times
    lo.trc              - trace
    lo.typ              - types
    lo.usr              - users

C O M M A N D S
===============

basic code is a function that gets an event as a argument:

::

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

::

 def command(event):
     event.reply("yooo %s" % event.origin)


You can add you own modules to the botd package and if you want you can
create your own package with commands in the botd namespace.


have fun coding ;]

| 

C O N T A C T
=============

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
