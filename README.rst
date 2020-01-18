R E A D M E
###########



BOTD is a IRC channel daemon and contains no copyright or LICENSE.



I N S T A L L



download the tarball from pypi, https://pypi.org/project/botd/#files

untar, cd into the directory and run:

::

 > ./bin/botirc localhost \#dunkbots botd

to have it connect to irc, join the channel and do nothing, users have to be !meet <nick> (on the console) before they can give commands.

you can also download with pip3 and install globally.

::

 > sudo pip3 install botd --upgrade

if you want to develop on the bot clone the source at github.:

::

 > git clone https://github.com/bthate/botd
 > cd botd
 > sudo python3 setup.py install

or run a bot locally:

::

 > ./bin/botd

if you want to have the daemon started at boot, run:

::

 > sudo init.d/install

this will install an botd service and starts BOTD on boot.



C O N F I G U R A T I O N



you can use the botctl program to configure BOTD:


::

 > botctl -d /var/lib/botd cfg krn modules rss,udp
 > botctl -d /var/lib/botd cfg irc server localhost
 > botctl -d /var/lib/botd cfg irc channel #botd
 > botctl -d /var/lib/botd meet ~bart@127.0.0.1
 > botctl -d /var/lib/botd rss https://news.ycombinator.com/rss



U D P



using udp to relay text into a channel, start the bot with -m udp and use
the botudp program to send text to the UDP to channel server:

::

 > tail -f ~/.bot/logs/bot.log | botudp 



M O D U L E S



BOTD contains the following modules:

::

 botd				- bot library.
 botd.bot			- bot base class.
 botd.cfg			- configuration command.
 botd.clk			- clock functions.
 botd.cmd			- basic commands
 botd.csl			- console.
 botd.dbs			- database.
 botd.dft			- default values.
 botd.ent			- log and todo commands.
 botd.err			- errors.
 botd.flt			- list of bots.
 botd.fnd			- search objects.
 botd.fnd			- search database.
 botd.gnr			- generic object functions.
 botd.hdl			- handler.
 botd.irc			- IRC bot.
 botd.krn			- kernel code.
 botd.ldr			- module loader.
 botd.log			- logging.
 botd.prs			- parsing of commands.
 botd.pst			- persitence.
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
    
