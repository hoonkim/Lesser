from bridge.bridge import Bridge
from unittest import TestCase
import random
import string
import sys
from bson import json_util

__author__ = 'honghee'


class TestBridge(TestCase):

    def test_dummy(self):
        bridge = Bridge()
        appName = "App5"
        c = string.digits + string.ascii_letters
        n = string.digits

        for i in range(1,12):
            ranIDLen = random.randint(1,10)
            ranPWLen = random.randint(1,10)
            ranNameLen = random.randint(0,5)
            ranID  = ''.join(random.sample(c,ranIDLen))
            ranPW  = ''.join(random.sample(c,ranPWLen))
            ranName = ''.join(random.sample(c,ranNameLen))
            ranPhone = "010"+str(''.join(random.sample(n,8)))
            ranAddress = ''.join(random.sample(c,ranNameLen))
            doc = { 'id':ranID,'pw':ranPW,'name':ranName,'phone':ranPhone,'address':ranAddress}
            #bridge.application(appName).schema('JoinPage').insert(doc)

        for i in range(1,60):
            ranIDLen = random.randint(1,10)
            ranPWLen = random.randint(1,10)
            ranNameLen = random.randint(0,5)
            ranID  = ''.join(random.sample(c,ranIDLen))
            ranPW  = ''.join(random.sample(c,ranPWLen))
            ranName = ''.join(random.sample(c,ranNameLen))
            ranPhone = "010"+str(''.join(random.sample(n,8)))
            ranAddress = ''.join(random.sample(c,ranNameLen))
            doc = { 'id':ranID,'pw':ranPW}
            #bridge.application(appName).schema('JoinPage').insert(doc)


        for i in range(1,80):
            ranIDLen = random.randint(1,10)
            ranPWLen = random.randint(1,10)
            ranNameLen = random.randint(0,5)
            ranID  = ''.join(random.sample(c,ranIDLen))
            ranPW  = ''.join(random.sample(c,ranPWLen))
            ranName = ''.join(random.sample(c,ranNameLen))
            ranPhone = "010"+str(''.join(random.sample(n,8)))
            ranAddress = ''.join(random.sample(c,ranNameLen))
            doc = { 'name':ranName,'phone':ranPhone}
            #bridge.application(appName).schema('JoinPage').insert(doc)

        data = json_util.dumps( bridge.application(appName).schema('JoinPage').find({'address':'6P'},{'pw':'0'}) )
        print(data)

        data = json_util.dumps( bridge.application(appName).schema('JoinPage').find({'address':'6P'}) )
        print(data)
