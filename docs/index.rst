R E A D M E
###########


BOTD is a IRC channel daemon serving 24/7 in the background, it installs it's own botd.service file and can thus survive reboots.
BOTD contains no copyright or LICENSE and is placed in the public domain.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botd/#files or
you can also download with pip3 and install globally:

::

 > sudo pip3 install botd --upgrade --force-reinstall


if you want the botd to start on boot after install run:

::

 > sudo cp botd.service /etc/systemd/system/botd.service
 > sudo botctl cfg <server> <channel> <nick> <owner>
 > sudo bothup

U S A G E

::

 > bot <cmd>		- executes a command
 > bot 			- starts a shell
 > botctl		- executes a command on the system botd
 > botd			- starts daemon
 > bothup		- restarts the botd service

logfiles can be found in /var/log/botd.


C O N F I G U R A T I O N


use "botctl cfg" (sudo) to edit on the system installed botd service.
IRC configuration uses the cfg command to edit server/channel/nick:

::

 > botctl cfg localhost #dunkbots botje ~bart@127.0.0.1


R S S

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

 > git clone https://bitbucket.org/botlib/botd

BOTD uses the BOTLIB library to run an irc bot in the background.

 > git clone https://bitbucket.org/botlib/botlib

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

.. toctree::
   :hidden:
   :glob:

   *
