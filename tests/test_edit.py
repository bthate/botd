# BOTD - python3 IRC channel daemon.
#
# edit tests.

import json
import logging
import os
import unittest

from bl.obj import Object
from bl.prs import Command
from bl.hdl import Event
from bl.utl import edit

class Log(Object):

    def __init__(self):
        self.txt = "bla"

l = Log()

class Test_Edit(unittest.TestCase):

    def setUp(self):
        l.txt = "bla"
        
    def test_edit1(self):
        e = Command()
        e.parse("ed log txt==bla txt=mekker")
        edit(l, e.setter)
        self.assertEqual(l.txt, "mekker")

    def test_edit2(self):
        e = Command()
        e.parse("ed")
        edit(l, e.setter)
        self.assertTrue(True, True)

    def test_edit3(self):
        e = Command()
        e.parse("ed log txt=#bla")
        edit(l, e.setter)
        self.assertEqual(l.txt, "#bla")

    def test_edit4(self):
        e = Command()
        e.parse("ed log txt==#bla txt=mekker2")
        edit(l, e.setter)
        self.assertEqual(l.txt, "mekker2")

    def test_edit5(self):
        e = Command()
        e.parse("ed log txt==mekker txt=bla1,bla2")
        edit(l, e.setter)
        self.assertEqual(l.txt, ["bla1", "bla2"])

    def test_edit(self):
        e = Command()
        e.parse("ed log txt==bla txt=#mekker")
        edit(l, e.setter)
        self.assertEqual(l.txt, "#mekker")
