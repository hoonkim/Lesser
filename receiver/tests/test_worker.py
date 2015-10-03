from unittest import TestCase
from receiver.worker import *

__author__ = 'kimothy'


class TestLesserWorker(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLesserWorker, self).__init__(*args, **kwargs)
        self.worker = LesserWorker()

    def test_work_process(self):
        work = LesserWork(ipaddress.ip_address('10.88.92.226'), 8000, HostProtocol.POST, "/", "{\"test\":33}")
        count = self.worker.GetWorkCount()

        self.worker.AddWork(work)

        self.assertEqual(self.worker.GetWorkCount(), count+1, "GetCountTest")
        self.assertEqual(str(self.worker.GetWork()), "<10.88.92.226/8000/POST///{\"test\":33}>")

        with self.assertRaises(Exception):
            self.worker.start()
            time.sleep(1)
            self.worker.exitWorker(self)
