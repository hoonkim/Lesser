import json
from bridge.hidden_app import HiddenApp

class DEFAULT_MACHINE:
    def __init__(self):
        self.addr ="mongodb://175.126.105.125"
        self.port=27017

class Bridge:

    def __init__(self, machine=None):
        self.appList = dict()
        self.appList['App1']=None
        if machine is None:
            machine = DEFAULT_MACHINE()
        self.__machine = machine

    def application(self, name):
        if self.appList.get(name) == None:
            self.appList[name] = HiddenApp(self.__machine)
            self.appList[name].connect(name)
        return self.appList[name]
  

    def createApp(self, name):
        self.appList[name] = HiddenApp().create(name)


        
