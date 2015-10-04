from receiver.worker import *
from db.controller import *

import sys
sys.path.append("../")
from users.usermanager import *


class LesserJob():
    def __init__(self):
        self.__worker = LesserWorker()

    def add_work(self, hostAddr, hostPort, hostProtocol, hostUrl, hostQuery, hostText, machine):
        work = LesserWork(ipaddress.ip_address(hostAddr), hostPort, HostProtocol(hostProtocol), hostUrl, hostQuery, hostText, machine)
        self.__worker.AddWork(work)

    def get_work(self):
        return self.__worker.GetWork()

    def start_work(self):
        self.__worker.start()

