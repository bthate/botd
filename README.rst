# BOTD - IRC channel daemon.
#
# setup.py

R E A D M E
###########

BOTD is a IRC channel daemon and contains no copyright or LICENSE.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botd/#files

untar, cd into the directory and run:

::

 > ./bin/botd localhost \#dunkbots botd

to have it connect to irc, join the channel and do nothing, users have to be !meet <nick> (on the console) before they can give commands.

you can also download with pip3 and install globally.

::

 > sudo pip3 install botd --upgrade

if you want to develop on the bot clone the source at github.:

::

 > git clone https://github.com/bthate/botd
 > cd botd
 > sudo python3 setup.py install

to run a bot:

::

 > botd -s  (starts a shell)
 > botd -x  (runs a command)
 > botd -d  (runs a daemon)
 > botd -z  (runs a service)

if you want to have the daemon started at boot, run:

::

 > sudo init.d/install

this will install a botd service and starts BOTD on boot.


C O N F I G U R A T I O N



to configure the BOTD service, you can use the config script with the following options:

 > sudo init.d/config <modules> <server> <channel> <nick> <owner>

for example:

 > sudo init.d/config irc,udp,rss,botd.cmd.shw irc.freenode.net #botd botd ~bart@shell.dds.nl

you can use the botd -x program option to configure BOTD:

::

 > botd -x cfg krn modules irc,rss
 > botd -x cfg irc server localhost
 > botd -x cfg irc channel #botd
 > botd -x meet ~bart@127.0.0.1
 > botd -x rss https://news.ycombinator.com/rss

use the -w option if you want to use a different work directory then ~/.botd, for example:

 > botd -w /var/lib/botd cfg irc server irc.freenode.net


U D P


using udp to relay text into a channel, start the bot with -m udp and use
the botudp program to send text to the UDP to channel server:

::

 > tail -f ~/.bot/logs/bot.log | botudp 


M O D U L E S


BOTD contains the following modules:

::

    botd			- bot library.
    botd.bot			- bot base class.
    botd.clk			- clock functions.
    botd.csl			- console.
    botd.dbs			- database.
    botd.dft			- default values.
    botd.err			- errors.
    botd.flt			- list of bots.
    botd.gnr			- generic object functions.
    botd.hdl			- handler.
    botd.irc			- IRC bot.
    botd.krn			- kernel code.
    botd.ldr			- module loader.
    botd.log			- logging.
    botd.prs			- parsing of commands.
    botd.rss			- fetch RSS feeds.
    botd.shl			- shell.
    botd.thr			- threads.
    botd.tms			- time related.
    botd.trc			- trace.
    botd.trm			- terminal code.
    botd.typ			- typing.
    botd.udp			- UDP packet to IRC channel relay.
    botd.usr			- user management.
    botd.utl			- utilities.
    botd.cmd.cfg		- config command.
    botd.cmd.cmd		- list of commands.
    botd.cmd.ent		- log and todo commands.
    botd.cmd.fnd		- find objects.
    botd.cmd.rss		- manage feeds.
    botd.cmd.shw		- show runtime data.
    botd.cmd.usr		- manage users.
 

C O D I N G


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


have fun coding ;]


I N F O


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
