import sys
from bridge.bridge import Bridge
from unittest import TestCase

__author__ = 'honghee'


class Machine():
    def __init__(self, addr, uuid, port):
        self.addr = addr
        self.uuid = uuid
        self.port = port

class TestBridge(TestCase):
    def test_dummy(self):

        bridge = Bridge()
        bridge.application('App1').Schema('JoinPage').find({"dd":"dd"})
        bridge.application('App1').Schema('JoinPage').find({"dd":"dd"},{"ddd":0,"dddd":0})
