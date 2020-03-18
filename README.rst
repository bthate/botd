R E A D M E
###########


BOTD is a IRC channel daemon serving 24/7 in the background.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botlib/#files

if you want to have BOTLIB started at boot, you need to have the tarball and run:

::

 > sudo bin/install

this will install an botd service in /etc/systemd/system


you can also download with pip3 and install globally.

::

 > sudo pip3 install botlib --upgrade --force-reinstall


U S A G E


local:

::

 > bot <cmd>
 > bot -s localhost \#dunkbots botje
 > bot cmds

global:

 > bin/install
 > botctl <cmd>

logfiles can be found in /var/log/botd.


C O N F I G U R A T I O N


use botctl (sudo) to edit on the system installed botd service.
IRC configuration uses the cfg command to edit server/channel/nick:

::

 > botctl cfg irc server localhost
 > botctl cfg irc channel #dunkbots
 > botctl cfg irc nick botje

use the -w option if you want to use a different work directory then /var/lib/botd.


R S S


make sure you have bot.rss added to your cfg.modules:

::

 > botctl cfg krn modules bot.rss


add an url:

::

 > botctl rss https://news.ycombinator.com/rss
 ok 1

 run the rss command to see what urls are registered:

 > botctl rss
 0 https://news.ycombinator.com/rss

 the fetch command can be used to poll the added feeds:

 > botctl fetch
 fetched 0


U D P

make sure you have bot.udp added to your cfg.modules:

::

 > botctl cfg krn modules bot.udp

using udp to relay text into a channel, use the botudp program to send text via the bot 
to the channel on the irc server:

::

 > tail -f /var/log/botd/botd.log | botudp 

to send a message to the IRC channel, send a udp packet to the bot:

::

 import socket

 def toudp(host, port, txt):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)


C O N T A C T


you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
