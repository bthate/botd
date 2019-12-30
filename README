R E A D M E


BOTD is a library to program bots and BOTD is a IRC channel bot daemon using
the BOTD library. BOTD contains no copyright or LICENSE (not does BOTD).


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botd/#files

untar, cd into the directory and run:

::

 > ./bin/bot -m rss,entry,show localhost \#dunkbots bot

to have it connect to irc, join the channel and do nothing, users have to be !meet <nick> before they can give commands.
BOTD does it self not depend, you might need to install feedparser yourself to have rss working.

you can also download with pip3 and install globally.

::

 > sudo pip3 install botd --upgrade

if you want to develop on the bot clone the source at github.:

::

 > git clone https://github.com/bthate/botd
 > cd botd
 > sudo python3 setup.py install


I R C


for IRC use <server> <channel> <nick> and the bot will connect and join the channel:

::

 > bot -m rss,entry,show irc.freenode.net \#dunkbots bot

you can use the -b option to start the bot in the background and logfiles can be found in ~/.bot/logs.


B O O T


if you want to have the daemon started at boot, run:

::

 > sudo init.d/install

this will install an botd service and starts BOTD on boot.


R S S


add url:

::

 > bot -x rss https://news.ycombinator.com/rss
 ok 1

you can use the find command to see what urls are registered:

::

 > bot -x rss
 0 https://news.ycombinator.com/rss



U D P


using udp to relay text into a channel, start the bot with -m udp and use
the obudp program to send text to the UDP to channel server:

::

 > tail -f ~/.bot/logs/bot.log | obudp 


U S E R S


the default shell user is root@shell and gives access to all the commands that are available.
if you want to use users to control access to commands use the --users option.

::

 > meet bart
 ~bart@localhost added.

you can also use the full userhost as a argument to meet:

::

 > meet user@server
 user user@server created


M O D U L E S


BOTD contains the following modules:

::


 bl			- bot library.
 bl.all			- contains all sub modules
 bl.bot		- bot base class.
 bl.clk			- clock functions.
 bl.csl			- console.
 bl.dbs			- database.
 bl.err			- errors.
 bl.flt			- list of bots.
 bl.evt			- event.
 bl.hdl			- handler.
 bl.ldr			- module loader.
 bl.log			- logging.
 bl.pst			- persitence.
 bl.shl			- shell.
 bl.tbl			- dispatch tables.
 bl.tms			- time related.
 bl.trm			- terminal code.
 bl.thr			- threads.
 bl.trc			- trace.
 bl.typ			- typing.
 bl.usr		- user management.
 bl.utl			- utilities.

::

 botd.cmd		- basic commands
 botd.ent		- log and todo commands.
 botd.irc		- IRC bot.
 botd.udp		- UDP packet to IRC channel relay.
 
C O D E


if you want to add your own modules to the bot, you can put your .py files in a "mods" directory and use the -m option to point to that directory.

::

 > botd -m mods

basic code is a function that gets an event as a argument:

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
    
