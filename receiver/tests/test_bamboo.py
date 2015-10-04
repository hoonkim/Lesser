from unittest import TestCase
from receiver.worker import *

__author__ = 'kimothy'


class TestLesserWork(TestCase):
    def test_class(self):
        work = LesserWork(ipaddress.ip_address('10.88.92.226'), 8000, HostProtocol.POST, "/", "{\"test\":33}")
        self.assertEqual(str(work), "<10.88.92.226/8000/POST///{\"test\":33}>")
