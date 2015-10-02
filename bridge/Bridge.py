import json
from HiddenApp import HiddenApp

class Bridge:

    def __init__(self):
        self.appList = dict()
        self.appList['App1']=None

    def application(self, name):
        if any(name in key for key in self.appList.keys()):
            if self.appList[name] == None:
                self.appList[name] = HiddenApp().connect(name)
            return self.appList[name]
        else:
            return None

    def createApp(self, name):
        self.appList[name] = HiddenApp().create(name)


        