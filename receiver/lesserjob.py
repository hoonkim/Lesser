from worker import *
from db.controller import *

class LesserJob():
    def __init__(self):
        self.__worker = LesserWorker()

    def AddWork(self, hostAddr, hostPort, hostProtocol, hostQuery, hostText):
        work = LesserWork(ipaddress.ip_address(hostAddr), hostPort, HostProtocol(hostProtocol), hostQuery, hostText)
        self.__worker.AddWork(work)

    def GetWork(self):
        return self.__worker.GetWork()

    def StartWork(self):
        self.__worker.start()

    def process(self):

        pass

