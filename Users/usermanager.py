import hashlib
import os

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

        if hashkey == None:
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
            if searchType == SearchType.ADDR and i.addr = searchValue:
                return i
            elif searchType == SearchType.UUID and i.uuid = searchValue:
                return i
            elif searchType == SearchType.PORT and i.port = searchValue:
                return i
        return None


class UserManager():
    def __init__(self):
        self.userlist = list()

    def loadUser(self):
        #TO DO: implement mongodb code here! :)

        return None

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


m = UserManager()

m.AppendUser("hello","world")
m.AppendUser("hello2","world")
m.AppendUser("hello3","world")
m.AppendUser("hello4","world")
m.AppendUser("hello5","world")
m.AppendUser("hello6","world")
m.AppendUser("hello7","world")
m.AppendUser("hello8","world")
m.AppendUser("hello9","world")

aa = m.searchUser("hello")

if aa != None:
    print(aa.GetUserHashKey())
else:
    print("None")
