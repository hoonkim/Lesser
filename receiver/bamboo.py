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
    __hostUrl = ""
    __hostQuery = ""
    __hostText = ""

    def __init__(self, addr, port, protocol, url, query, text, machine):
        self.__hostAddr = addr
        self.__hostPort = port
        self.__hostProtocol = protocol
        self.__hostUrl = url
        self.__hostQuery = query
        self.__hostText = text
        self.__machine = machine

    def __str__(self):
        return "<" + str(self.__hostAddr) +"/"+ str(self.__hostPort) +"/"+ self.__hostProtocol.name +"/"+ self.__hostUrl +"/"+ str(self.__hostQuery) +"/" + self.__hostText + ">"

    def getProtocol(self):
        return self.__hostProtocol

    def getQuery(self):
        return self.__hostQuery

    def getText(self):
        return self.__hostText

    def getMachine(self):
        return self.__machine


class ProtocolException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)