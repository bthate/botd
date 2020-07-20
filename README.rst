B  O  T  D
##########

| Welcome to BOTD, the 24/7 channel daemon ! see https://pypi.org/project/botd/ 

BOTD can serve as a 24/7 background daaemon in an IRC channel, it can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to 
let it restart after reboots.
BOT is has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTD truely free (pastable) code you can use how you see fit, 

INSTALL
=======

you can download with pip3 and install globally:

::

 $ sudo pip3 install botd

You can download the tarball from https://pypi.org/project/botd/#files

if you want to develop on the botd clone the source at bitbucket.org:

::

 $ git clone https://bitbucket.org/bthate/botd

USAGE
=====

BOTD has it's own CLI, you can run it by giving the botd command on the
prompt, it will return with no response:

:: 

 $ botd
 $ 

you can use botd <cmd> to run a command directly:

::

 $ botd cmds
 cfg|cmd|dne|edt|fnd|flt|krn|log|add|tsk|tdo|udp|upt|ver

configuration is done with the cfg command:

::

 $ botd cfg
 channel=#botlib nick=botd port=6667 realname=botd server=localhost username=botd

you can use setters to edit fields in a configuration:

::

 $ botd cfg server=irc.freenode.net channel=\#dunkbots nick=botd
 channel=#dunkbots nick=botje port=6667 realname=botlib server=irc.freenode.net
 username=botlib

to start a irc server with the cmd and opr modules loaded and a console
running:

::

 $ botd mods=irc,csl,cmd,opr
 > ps
 0 0s       Console.input
 1 0s       IRC.handler
 2 0s       IRC.input
 3 0s       IRC.output
 4 0s       Kernel.handler
 > 

to run a pure UDP to IRC relay, run the bot with irc,udp modules loaded

::

 $ botd mods=irc,udp
 >

use the udp command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | botd udp

to send a udp packet to the bot:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

you can use the mods= setter to set the modules to load:

::

 $ botd mods=csl,cmd,opr
 > cmd
 cfg|cmd|flt|fnd|krn|tsk|upt|ver

BOTD has the following modules:

::

    clk             - clock/repeater
    cmd             - commands
    csl             - console
    dbs             - database
    err		    - errors
    flt             - list of bots
    hdl             - handler
    irc             - internet relay chat
    isp             - introspect
    krn             - core handler
    obj             - base classes
    opr             - opers
    mbx		    - email
    prs             - parse
    spc		    - specifications
    thr             - threads
    tms             - time
    trc             - trace
    udp             - udp to channel
    usr             - users
    utl             - utilities

you can add you own modules to the botd package, its a namespace package.

SERVICE
=======

if you want to run the bot 24/7 you can install BOTD as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::

 [Unit]
 Description=BOTD - the 24/7 channel daemon
 After=network-online.target
 Wants=network-online.target
 
 [Service]
 ExecStart=/usr/local/bin/botd mods=irc,udp
 
 [Install]
 WantedBy=multi-user.target

then add the botd service with:

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

BOTD detects whether it is run as root or as a user. if it's root it
will use the /var/lib/botd/ directory and if it's user it will use ~/.botd

CONTACT
=======

contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

