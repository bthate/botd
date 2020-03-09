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


::

 > bot localhost \#dunkbots botje
 > botsh
 > botd 
 > botcmd <cmd>
 > botctl <cmd>

logfiles can be found in /var/log/botd.


C O N F I G U R A T I O N


use botctl to edit on the system installed botd service:

::

 > sudo botctl cfg krn modules bot.rss,bot.udp
 > sudo botctl cfg irc server localhost
 > sudo botctl cfg irc channel #dunkbots
 > sudo botctl cfg irc nick botje
 > sudo botctl rss https://news.ycombinator.com/rss

use the -w option if you want to use a different work directory then /var/lib/botd.


R S S


add an url:

::

 > sudo botctl rss https://news.ycombinator.com/rss
 ok 1

 run the rss command to see what urls are registered:

 > sudo botctl rss
 0 https://news.ycombinator.com/rss

 the fetch command can be used to poll the added feeds:

 > sudo botctl fetch
 fetched 0


U D P


using udp to relay text into a channel, start the bot with -m bot.udp and use
the botudp program to send text via the bot to the channel on the irc server:

::

 > tail -f /var/log/botd/botd.log | botudp 


C O D I N G


if you want to develop on the library clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/botlib
 > cd botlib
 > sudo python3 setup.py install

if you want to add your own modules to the bot, you can put you .py files in a "mods" directory and use the -m option to point to that directory.

BOTLIB contains the following modules:

::

    bot.dft		- default
    bot.flt		- fleet
    bot.irc		- irc bot
    bot.krn		- core handler
    bot.rss		- rss to channel
    bot.shw		- show runtime
    bot.udp		- udp to channel
    bot.usr		- users

BOTLIB uses the LIBOBJ library which gets included in the tarball.

::

    lo.clk		- clock
    lo.csl		- console 
    lo.hdl		- handler
    lo.shl		- shell
    lo.thr		- threads
    lo.tms		- times
    lo.typ		- types

basic code is a function that gets an event as a argument:

::

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

::

 def command(event):
     event.reply("yooo %s" % event.origin)


have fun coding ;]


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
