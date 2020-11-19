README
######

Welcome to BOTD,

BOTD is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. It installs itself as a service so
you can get it restarted on reboot. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it, have it log objects on
disk and search them and scan emails for correspondence analysis. BOTD uses
a JSON in file database with a versioned readonly storage. It reconstructs
objects based on type information in the path and uses a "dump OOP and use
OP" programming library where the methods are factored out into functions
that use the object as the first argument. BOTD is placed in the Public
Domain and has no COPYRIGHT or LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install botd

if you have previous versions already installed and things fail try to force reinstall:

::

 > sudo pip3 install botd --upgrade --force-reinstall

if this also doesn't work you'll need to remove all installed previous  versions, so you can do a clean install.

you can run directly from the tarball, see https://pypi.org/project/botd/#files

SERVICE
=======

if you want to run the bot 24/7 you can install BOTD as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::

 [Unit]
 Description=BOTD - 24/7 channel daemon
 After=network-online.target

 [Service]
 DynamicUser=True
 StateDirectory=botd
 LogsDirectory=botd
 CacheDirectory=botd
 ExecStart=/usr/local/bin/botd
 CapabilityBoundingSet=CAP_NET_RAW

 [Install]
 WantedBy=multi-user.target

then enable the botd service with:

::

 $ sudo systemctl enable botd
 $ sudo systemctl daemon-reload

to configure the bot use the cfg (config) command (see above). use sudo for the system
daemon and without sudo if you want to run the bot locally. then restart
the botd service.

::

 $ sudo service botd stop
 $ sudo service botd start

if you don't want botd to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/botd.service


USAGE
=====

BOTD havs it's own CLI, the botctl program. It needs root because the botd
program uses systemd to get it started after a reboot. You can run it on the shell
prompt and, as default, it won't do anything.

:: 

 $ sudo botctl
 $ 

you can use botctl <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ sudo botctl cmd
 cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver


IRC
===

configuration is done with the cfg command:

::

 $ sudo botctl cfg
 channel=#botd nick=botd port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ .sudo botctl cfg server=irc.freenode.net channel=\#dunkbots nick=botd
 channel=#dunkbots nick=botd port=6667 server=irc.freenode.net

to have the irc bot started use the mods=irc option at start:

::

 $ sudo botd mods=irc

RSS
===

BOTD provides with the use of feedparser the possibility to server rss
feeds in your channel. To add an url use the rss command with an url:

::

 $ sudo botctl rss https://github.com/bthate/botd/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ sudo botctl fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ sudo botctl ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller.

::

 $ sudo botd mods=irc,rss

UDP
===

BOTD also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

use the 'botudp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | botudp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to botd, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to botd in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

CONTACT
=======

"hope you enjoy my contribution back to society."

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
