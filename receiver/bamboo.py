from enum import Enum
import ipaddress
from pymongo import MongoClient
import json
from bridge.bridge import Bridge


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

    def process(self):
        if self.__hostProtocol is HostProtocol.GET :
            self.get()
        elif self.__hostProtocol is HostProtocol.POST:
            self.post()

    def get(self):
        #client = MongoClient(self.__machine.addr, self.__machine.port )
        #db = client.db
        #result = db[self.__hostUrl].find(self.__hostQuery)
        bridge = Bridge(self.__machine)
        result = bridge.application('lesser').schema(self.__hostUrl).find(self.__hostQuery)
        print(result)


        return result

    def post(self):
        #client = MongoClient(self.__machine.addr, self.__machine.port )
        #db = client.db
        #result = {'object_id' : db[self.__hostUrl].insert(self.__hostText).inserted_id}
        bridge = Bridge(self.__machine)
        result = {'object_id' :
                      bridge.application('lesser')
                          .schema(self.__hostUrl)
                          .insert(self.__hostText).inserted_id
                  }

        print(result)

        return result



class ProtocolException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
