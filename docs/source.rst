.. _source:

SOURCE
======

BOTLIB contains the following modules:

.. autosummary::
    :toctree: 
    :template: module.rst

    bot.clk             - clock/repeater
    bot.csl             - console
    bot.fil             - file 
    bot.hdl             - handler
    bot.irc             - internet relay chat
    bot.itr             - introspect
    bot.krn             - core handler
    bot.obj             - base classes
    bot.prs             - parse
    bot.shl             - shell
    bot.thr             - threads
    bot.tms             - time
    bot.trc             - trace


BOTD itself provides these modules:

.. autosummary::
    :toctree: 
    :template: module.rst


    botd.cmd             - commands
    botd.opr             - opers
    botd.rss             - rich site syndicate
    botd.udp             - udp to channel

You can add you own modules to the botd package, its a namespace package.
