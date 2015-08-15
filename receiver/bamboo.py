from enum import Enum
import ipaddress

class HostProtocol(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    OPTION = 4
    HEADER = 5


class LesserWork():
    __hostAddr = ipaddress.ip_address('127.0.0.1')
    __hostPort = 8080
    __hostProtocol = HostProtocol.GET
    __hostQuery = ""
    __hostText = ""

    def __init__(self, addr, port, protocol, query, text):
        self.__hostAddr = addr
        self.__hostPort = port
        self.__hostProtocol = protocol
        self.__hostQuery = query
        self.__hostText = text

    def __str__(self):
        return "<" + str(self.__hostAddr) +"/"+ str(self.__hostPort) +"/"+ self.__hostProtocol.name +"/"+ self.__hostQuery +"/" + self.__hostText + ">"