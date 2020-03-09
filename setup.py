# BOTD - IRC channel daemon.
#
# setup.py

from setuptools import setup, find_namespace_packages

setup(
    name='botd',
    version='9',
    url='https://bitbucket.org/botd/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTD is a IRC channel daemon serving 24/7 in the background.. no copyright. no LICENSE.",
    long_description="""
R E A D M E
###########


BOTD is a library you can use to program bots. no copyright. no LICENSE.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botd/#files

if you want to have BOTD started at boot, you need to have the tarball and run:

::

 > sudo bin/install

this will install an botd service in /etc/systemd/system


you can also download with pip3 and install globally.

::

 > sudo pip3 install botd --upgrade --force-reinstall



U S A G E


::

 > sudo botd localhost \#dunkbots botje
 > sudo botctl <cmd>

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


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
    
    """,
    long_description_content_type="text/x-rst",
    license='Public Domain',
    install_requires=["botlib", "feedparser"],
    zip_safe=True,
    packages=["botd"],
    scripts=["bin/botd", "bin/botctl", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
