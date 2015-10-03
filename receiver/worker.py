import threading
from queue import Queue
import time
from bamboo import *

class LesserWorker(threading.Thread):
    __q = Queue()

    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def AddWork(self, work):
        self.__q.put(work)

    def GetWork(self):
        a = self.__q.get()
        return a

    def GetWorkCount(self):
        return self.__q.qsize()

    
    def run(self):
        while True:
            while self.__suspend:
                time.sleep(0.5)

            work = self.__q.get()
            ## process here ##
            #for debug
            print(work)

            work.getMachine()
            
            if self.__exit:
                break

    def suspendWorker(self):
        self.__suspend = True
         
    def resumeWorker(self):
        self.__suspend = False
         
    def exitWorker(self):
        self.__exit = True

