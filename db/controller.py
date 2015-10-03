__author__ = 'HoonKim'

from pymongo import MongoClient
from http_parser import *

class Mongo:

    def __init__(self):
        self.__connections = {}

    def getDB(self, machine):
        if machine.uuid not in self.__connections :
            connection = {
                'machine' : machine,
                'db' : MongoClient(machine.addr, machine.port)
            }

        return connection[machine.uuid]

    def getConnectionCount(self) :
        return len(self.__conections)

    def insert(self, schema, body, machine) :
        return self.getDB(machine)[schema].insert(body)

    def find(self, schema, condition, machine):
        return self.getDB(machine)[schema].find(condition)






