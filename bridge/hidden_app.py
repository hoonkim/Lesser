﻿import json
import pymongo
from bridge.convert_column import ConvertColumn
from bridge.collections.collection_controller import CollectionController
from bridge.schema import Schema


class HiddenApp: 

    def __init__(self, machine):
        self.schemaList = dict()
        self.columnList = dict()
        self.THRESHOLD = 50;
        self.pushCount = 0;
        self.__machine = machine

    def schema(self, name): 
        if self.schemaList.get(name) != None:
            return self.schemaList.get(name)
        else:
            self.db['SchemaList'].insert({'URL':name, 'column':[],'child':[]})
            self.schemaList[name] = Schema({'URL':name, 'column':[],'child':[]},self.db,self.push)
            return self.schemaList[name]

    def connect(self, name):
        
        self.db = pymongo.MongoClient(self.__machine.addr, int(self.__machine.port))[name]
        self.collectionController = CollectionController(self.db)

        self.columnList = list()   
        self.convertColumn = ConvertColumn(self.columnList,self.db )     
         
        if self.db['ColumnList'] !=None:
            cursor = self.db.ColumnList.find()
            for document in cursor:
                self.columnList.append(document["column"])

        if self.db['SchemaList'] !=None:
            cursor = self.db.SchemaList.find()
            for document in cursor:
                self.schemaList[document["URL"]] = Schema(document,self.db,self.push)
        
    def push(self, type, keys):
        print("Push count : ", self.pushCount)
        self.pushCount +=1
        key = self.convertColumn.columnsToIdxString(keys)
        self.collectionController.Push(type , key)

        if self.pushCount> self.THRESHOLD :
            self.pushCount = 0
            cursor = self.db.SchemaList.find()
            beforeSchemaList = list()
            for document in cursor:
                beforeSchemaList.append(document)
            newSchemaList = self.collectionController.Run(beforeSchemaList, self.columnList)
            for newSchema in newSchemaList:
                print(newSchema)  
                beforeSchema = self.schemaList[newSchema['URL']].schemaValue
                for child in beforeSchema['child']:
                    self.db[child['URL']].drop()
                self.db[beforeSchema['URL']].drop()

                cursor = self.db[beforeSchema['URL']+"_default"].find()
                newData=dict()
                for data in cursor:
                    newData.clear()
                    for column in newSchema['column']:
                        if column in data:
                            newData[column] = data[column]
                    pk = self.db[newSchema['URL']].insert_one(newData).inserted_id
                    for child in newSchema['child']:
                        newData.clear()
                        for column in child['column']:
                            if column in data:
                                newData[column] = data[column]
                        if len(newData.keys())==0:
                            continue
                        newData['fk'] = pk
                        self.db[child['URL']].insert_one(newData)

                self.schemaList[newSchema['URL']].setSchemaValue(newSchema)
                #update db schema
                self.db['SchemaList'].remove({'URL':beforeSchema['URL']})
                self.db['SchemaList'].insert(newSchema)