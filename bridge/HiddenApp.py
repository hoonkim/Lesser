import json
import pymongo
from bridge.ConvertColumn import ConvertColumn 
from bridge.collections.CollectionController import CollectionController
from bridge.Schema import Schema


class HiddenApp: 

    def __init__(self): 
        self.schemaList = dict()
        self.columnList = dict()
        self.THRESHOLD = 10000;
        self.pushCount = 0;
        self.convertColumn = ConvertColumn()

    def schema(self, name):
        return self.schemaList[name]

    def connect(self, name):
        
        self.db = pymongo.MongoClient("mongodb://175.126.105.125:27017")[name]
        
        self.collectionController = CollectionController(self.db)
        #db에서 schemaList/ columnList/ hashCount를 가져옴
        self.hashCount = dict()     #DB get Hash Count
        cursor = self.db.HashCount.find()
        for document in cursor:
            self.HashCount[document["hashStr"]] = document["count"]

        for key in self.schemaList.keys():
            self.schemaList[key] = Schema(key,db,self.push)
        pass

    def create(self, name):
        #따로 넣을게없는듯?
        pass

    def push(self, type, keys):
        self.pushCount +=1
        key = self.convertColumn.columnsToIdxString(keys)
        self.collectionController.Push(type , key)

        if self.pushCount> self.THRESHOLD :
            self.pushCount = 0
            self.collectionController.Run()
