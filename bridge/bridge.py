import json
from HiddenApp import HiddenApp

class Bridge:

    def __init__(self):
        self.appList = dict()
        self.appList['App1']=None

    def application(self, name):
        if self.appList.get(name) == None:
            self.appList[name] = HiddenApp()
            self.appList[name].connect(name)
        return self.appList[name]
        #if any(name == key for key in self.appList.keys()):
        #    if self.appList.get(name) == None:
        #        self.appList[name] = HiddenApp()
        #        self.appList[name].connect(name)
        #    return self.appList[name]
        #else:
        #    return None

    def createApp(self, name):
        self.appList[name] = HiddenApp().create(name)


        
