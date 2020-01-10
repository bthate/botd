# BOTD - python3 IRC channel daemon.
#
# setup.py

from setuptools import setup

setup(
    name='botd',
    version='1',
    url='https://bitbucket.org/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="python3 IRC channel daemon.",
    long_description="""
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

if you want to have the daemon started at boot, run:

::

 > sudo init.d/install

this will install an botd service and starts BOTD on boot.


C O N F I G U R A T I O N


you can use the botctl program to configure BOTD:


::

 > botctl -d /var/lib/botd cfg krn modules cmd,ent,rss,shw,udp
 > botctl -d /var/lib/botd cfg irc server localhost
 > botctl -d /var/lib/botd cfg irc channel #botd
 > botctl -d /var/lib/botd meet ~bart@127.0.0.1
 > botctl -d /var/lib/botd rss https://news.ycombinator.com/rss


U D P


using udp to relay text into a channel, start the bot with -m udp and use
the toudp program to send text to the UDP to channel server:

::

 > tail -f ~/.bot/logs/bot.log | toudp 


M O D U L E S


BOTD contains the following modules:

::

 botd				- bot library.
 botd.bot			- bot base class.
 botd.clk			- clock functions.
 botd.cmd			- basic commands
 botd.csl			- console.
 botd.dbs			- database.
 botd.ent			- log and todo commands.
 botd.err			- errors.
 botd.flt			- list of bots.
 botd.evt			- event.
 botd.hdl			- handler.
 botd.irc			- IRC bot.
 botd.ldr			- module loader.
 botd.log			- logging.
 botd.pst			- persitence.
 botd.shl			- shell.
 botd.tbl			- dispatch tables.
 botd.tms			- time related.
 botd.trm			- terminal code.
 botd.thr			- threads.
 botd.trc			- trace.
 botd.typ			- typing.
 botd.udp			- UDP packet to IRC channel relay.
 botd.usr			- user management.
 botd.utl			- utilities.
 

basic code for a command is a function that gets an event as a argument:

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
    
    
    """,
    license='Public Domain',
    install_requires=["feedparser"],
    packages=["botd"],
    scripts=["bin/botd", "bin/botctl", "bin/botirc", "bin/botsh", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
