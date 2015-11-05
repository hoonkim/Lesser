import hashlib
import os
from enum import Enum
from pymongo import MongoClient

SALT_KEY = 183

class SearchType(Enum):
    ADDR = 0
    UUID = 1
    PORT = 2

class Machine():
    def __init__(self, addr, uuid, port):
        self.addr = addr
        self.uuid = uuid
        self.port = port


class User():
    def __init__(self, username, password, hashKey):
        self.username = username
        salt = os.urandom(SALT_KEY)

        self.machineList = list()

        if hashKey == None:
            self.userpassword = hashlib.md5((password+str(salt)).encode()).hexdigest()
            self.userHashKey = hashlib.md5((username+str(salt)).encode()).hexdigest()
        else:
            self.userpassword = password
            self.userHashKey = hashKey


    def GetUsername(self):
        return self.username

    def GetPassword(self):
        return self.userpassword

    def GetUserHashKey(self):
        return self.userHashKey

    def AddMachine(self, machine):
        self.machineList.append(machine)
    
    def findMachine(self, searchType, searchValue):
        for i in self.machineList:
            if searchType == SearchType.ADDR and i.addr == searchValue:
                return i
            elif searchType == SearchType.UUID and i.uuid == searchValue:
                return i
            elif searchType == SearchType.PORT and i.port == searchValue:
                return i
        return None

    def getFirstMachine(self):
        if len(self.machineList) == 0:
            return None
        else:
            return self.machineList[0]


class UserManager():

    __mongoIp = 'localhost'
    __mongoPort = 27017

    def __init__(self):
        self.userlist = list()

    def loadUser(self):
        client = MongoClient(self.__mongoIp, self.__mongoPort)
        userList = client['lesser']['users'].find()
        print("Applist load")

        for user in userList :
            print(user['username'])
            self.AppendUser(user['username'],
                            user['password'],
                            user['hashkey'])

        client.close()

    #if exist user contain hashKey Value.
    def AppendUser(self, username, password, hashKey):
        if self.searchUser(username) == None:
            tempUser = User(username, password, hashKey)
            self.userlist.append(tempUser)
            return tempUser
        return None

    def searchUser(self, username):
        for i in self.userlist:
            if i.GetUsername() == username:
                return i
        return None
