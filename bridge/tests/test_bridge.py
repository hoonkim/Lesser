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

        c = string.digits + string.ascii_letters
        n = string.digits

        for i in range(1,10):
            ranIDLen = random.randint(1,10)
            ranPWLen = random.randint(1,10)
            ranNameLen = random.randint(0,5)
            ranID  = ''.join(random.sample(c,ranIDLen))
            ranPW  = ''.join(random.sample(c,ranPWLen))
            ranName = ''.join(random.sample(c,ranNameLen))
            ranPhone = "010"+str(''.join(random.sample(n,8)))
            ranAddress = ''.join(random.sample(c,ranNameLen))
            doc = { 'id':ranID,'pw':ranPW,'name':ranName,'phone':ranPhone,'address':ranAddress}
#            doc = { 'name':ranName,'phone':ranPhone,'address':ranAddress}
#            doc = {'address':ranAddress}
#            doc = { 'id':ranID, 'address':ranAddress}
            try:
                pass
#                bridge.application('App3').schema('JoinPage').insert(doc)
            except:
                 print ("insert faild", sys.exc_info()[0])


        cursor = bridge.application('App3').schema('JoinPage').find({'phone':"01017935084"},{'name':1})
        data = json_util.dumps(cursor)
        print(data)

#        for i in range(1,50):
 #           bridge.application('App3').schema('JoinPage').find({'id':'1'},{'pw':'0'})

 #       for i in range(1,80):
 #           bridge.application('App3').schema('JoinPage').find({'name':'1'},{ 'phone':'0'})