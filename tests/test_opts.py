# BOTD - python3 IRC channel daemon.
#
# configuration tests

import unittest

from bl.krn import Cfg
from bl.obj import Default, Object
from bl.shl import make_opts

opts = [
    ('-d', '--datadir', 'store', str, 'set working directory.', 'workdir'),
    ('-m', '--modules', 'store', str, 'modules to load.', 'modules'),
    ('-o', '--options', "store", str, "options to use.", 'options'),
    ('-l', '--loglevel', 'store', str, 'set loglevel.', 'level'),
    ('-v', '--verbose', 'store_true', False, 'enable verbose mode.', 'verbose'),
    ('-z', '--shell', 'store_false', True, 'enable shell.', 'shell')
]

class O(Default):

    def bla(self):
        return "yo!"

class Test_Opts(unittest.TestCase):

    def test_options1(self):
        cfg = Object()
        print(cfg)
        make_opts(cfg, opts)
        print(cfg)
        self.assertTrue(cfg.shell)

