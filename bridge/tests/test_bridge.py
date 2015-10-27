from bridge.bridge import Bridge
from unittest import TestCase
import random
import string
import sys

__author__ = 'honghee'


class TestBridge(TestCase):

    def test_dummy(self):
        #스키마 분할 생각 전에 1. 테스트유닛 만들기
        # 2. find / insert 의 매개변수를 그냥 json data로 가정하고 1개 / 2개 일 때 고려하여 코딩
        # 3. 스키마의 schemaList 만든 후 tree 구조로 변경하기.
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
#            doc = { 'id':ranID,'pw':ranPW,'name':ranName,'phone':ranPhone,'address':ranAddress}
#            doc = { 'name':ranName,'phone':ranPhone,'address':ranAddress}
#            doc = {'address':ranAddress}
            doc = { 'id':ranID, 'address':ranAddress}
            try:
                bridge.application('App2').schema('JoinPage').insert(doc);
            except:
                 print ("insert faild", sys.exc_info()[0])

#        for i in range(1,50):
#            bridge.application('App2').schema('JoinPage').find({'id':'1', 'pw':'2'})

#        for i in range(1,80):
#            bridge.application('App2').schema('JoinPage').find({'name':'1', 'phone':'2'})