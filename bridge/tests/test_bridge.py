import sys
from bridge.bridge import Bridge
from unittest import TestCase


__author__ = 'honghee'


class TestBridge(TestCase):

    def test_dummy(self):
        bridge = Bridge()
        bridge.application('App1').Schema('JoinPage').find({"id":"sf","pw":"WJ"}); 