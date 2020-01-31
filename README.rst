R E A D M E
###########

BOTD is a IRC channel daemon and contains no copyright or LICENSE, source is :ref:`here <source>`


I N S T A L L
=============

download the tarball from pypi, https://pypi.org/project/botd/#files

untar, cd into the directory and run:

::

 > ./bin/botirc localhost \#dunkbots botd

to have it connect to irc, join the channel and do nothing, users have to be !meet <nick> (on the console) before they can give commands.

you can also download with pip3 and install globally.

::

 > sudo pip3 install botd --upgrade

if you want to develop on the bot clone the source at bitbucket.org.

::

 > git clone https://bitbucket.org/botd/botd
 > cd botd
 > sudo python3 setup.py install

if you want to have the daemon started at boot, run:

::

 > sudo init.d/install

this will install an botd service and starts BOTD on boot.

C O N F I G U R A T I O N
=========================

you can use the botctl program to configure BOTD:

::

 > botctl cfg krn modules rss,udp
 > botctl cfg irc server localhost
 > botctl cfg irc channel #botd
 > botctl meet ~bart@127.0.0.1
 > botctl rss https://news.ycombinator.com/rss

the botctl program takes normal bot commands and executes them. you can use the -d
option to use it on other then the default ~/.botd directory.

U D P
=====

using udp to relay text into a channel, start the bot with -m udp and use
the botudp program to send text to the UDP to channel server:

::

 > tail -f ~/.botd/logs/botd.log | botudp 

C O D I N G
===========

you can write your own modules for the bot, create a mod directory, put your 
.py file in there and load the module with -m mods. basic code for a command
is a function that gets an event as a argument:

::

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

::

 def command(event):
     event.reply("yooo %s" % event.origin)


I N F O
=======

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
|
| http:/pypi.org/project/botd

