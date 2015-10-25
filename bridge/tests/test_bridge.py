import sys
from bridge.bridge import Bridge
from unittest import TestCase

__author__ = 'honghee'


class TestBridge(TestCase):
    def test_dummy(self):
        queryList = [
            {"t1": "v1", "t2": "v2"}
            , {"_id": 0}
        ]

        bridge = Bridge()
        bridge.application('App1').Schema('JoinPage').find(queryList)
