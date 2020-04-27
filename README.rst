R E A D M E
###########


if you have problems with rebooting, remove the
/etc/systemd/system/botd.service file and see if box/node/host boots again.

BOTD is a IRC channel daemon serving 24/7 in the background,
it installs it's own botd.service file and can thus survive reboots.
BOTD contains no copyright or LICENSE and is placed in the public domain.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botd/#files
untar the tarball and run this to install the bot daemon on your system.

::

 > cd botd-13
 > sudo python3 setup.py install

you can also download with pip3 and install globally:

::

 > sudo pip3 install botd --upgrade --force-reinstall


if you don't want the botd to start on boot after install run:

::

 > sudo rm /etc/systemd/system/botd.service


run export PYTHONPATH="." and the bin should run directly
from the 


U S A G E

::

 > bot <cmd>		- executes a command
 > bot 			- starts a shell
 > botctl		- executes a command on the system botd
 > botcfg		- configure the bot, use botcfg <server> <channel> <nick>
 > botd			- starts daemon
 > bothup		- restarts the botd service

logfiles can be found in /var/log/botd.


C O N F I G U R A T I O N


use botcfg (sudo) to edit on the system installed botd service.
IRC configuration uses the cfg command to edit server/channel/nick:

::

 > botcfg localhost #dunkbots botje


R S S

the rss plugin uses the feedparser package, you need to install that
yourself:

::

 > pip3 install feedparser

make sure you have bot.rss added to your cfg.modules:

::

 > botctl cfg krn modules bot.rss


 add an url:

 > botctl rss https://news.ycombinator.com/rss
 ok 1

 run the rss command to see what urls are registered:

 > botctl rss
 0 https://news.ycombinator.com/rss

 the fetch command can be used to poll the added feeds:

 > botctl fetch
 fetched 0


U D P


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


C O D I N G


if you want to develop on the bot clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/botd


BOTLIB contains the following modules:

::

    bot.dft             - default
    bot.flt             - fleet
    bot.irc             - irc bot
    bot.krn             - core handler
    bot.rss             - rss to channel
    bot.shw             - show runtime
    bot.udp             - udp to channel
    bot.usr             - users

BOTLIB uses the LIBOBJ library which gets included in the tarball.

::

    lo.clk              - clock
    lo.csl              - console 
    lo.hdl              - handler
    lo.shl              - shell
    lo.thr              - threads
    lo.tms              - times
    lo.trc		- trace
    lo.typ              - types

basic code is a function that gets an event as a argument:

::

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

::

 def command(event):
     event.reply("yooo %s" % event.origin)


have fun coding ;]



C O N T A C T


you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
