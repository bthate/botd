""" edit command tests. """

import json
import logging
import ob
import os
import unittest

from ob.evt import Event
from ob.pst import Persist

class Log(Persist):

    """ check class attribute edit as well. """

    def __init__(self):
        self.txt = "bla"

l = Log()

def edit(obj, setter):
    """ edit an objects with the setters key/value. """
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        count += 1
        if "," in value:
            value = value.split(",")
        if value in ["True", "true"]:
            ob.set(obj, key, True)
        elif value in ["False", "false"]:
            ob.set(obj, key, False)
        else:
            ob.set(obj, key, value)
    return count

class Test_Edit(unittest.TestCase):

    def setUp(self):
        l.txt = "bla"
        
    def test_edit1(self):
        e = Event()
        e.parse("ed log txt==bla txt=mekker")
        edit(l, e.setter)
        self.assertEqual(l.txt, "mekker")

    def test_edit2(self):
        e = Event()
        e.parse("ed")
        edit(l, e.setter)
        self.assertTrue(True, True)

    def test_edit3(self):
        e = Event()
        e.parse("ed log txt=#bla")
        edit(l, e.setter)
        self.assertEqual(l.txt, "#bla")

    def test_edit4(self):
        e = Event()
        e.parse("ed log txt==#bla txt=mekker2")
        edit(l, e.setter)
        self.assertEqual(l.txt, "mekker2")

    def test_edit5(self):
        e = Event()
        e.parse("ed log txt==mekker txt=bla1,bla2")
        edit(l, e.setter)
        self.assertEqual(l.txt, ["bla1", "bla2"])

    def test_edit(self):
        e = Event()
        e.parse("ed log txt==bla txt=#mekker")
        edit(l, e.setter)
        self.assertEqual(l.txt, "#mekker")
