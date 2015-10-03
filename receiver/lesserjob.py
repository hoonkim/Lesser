from worker import *
from db.controller import *

import sys
sys.path.append("../")
from users.usermanager import *

class LesserJob():
    def __init__(self):
        self.__worker = LesserWorker()
        self.__protocol_table = {
            HostProtocol.GET : self.get,
            HostProtocol.POST: self.post
        }

    def AddWork(self, hostAddr, hostPort, hostProtocol, hostQuery, hostText, machine):
        work = LesserWork(ipaddress.ip_address(hostAddr), hostPort, HostProtocol(hostProtocol), hostQuery, hostText, machine)
        self.__worker.AddWork(work)

    def GetWork(self):
        return self.__worker.GetWork()

    def StartWork(self):
        self.__worker.start()

    def process(self):
        work = self._worker.GetWork()

        protocol = work.getProtocol

        if work.getProtocol() > HostProtocol.GET :
            raise ProtocolException("Unsupported Protocol")

        self.__protocol_table[protocol]()

    def get(self):
        pass

    def post(self):
        pass
