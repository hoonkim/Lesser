import json
from bridge.hidden_app import HiddenApp


class Bridge:

    def __init__(self):
        self.appList = dict()
        self.appList['App1']=None

    def application(self, name):
        if self.appList.get(name) == None:
            self.appList[name] = HiddenApp()
            self.appList[name].connect(name)
        return self.appList[name]
  

    def createApp(self, name):
        self.appList[name] = HiddenApp().create(name)


        
