from Collections.Apriori import Apriori
from Collections.Indexings import Indexing
import pymongo

class CollectionController:

    def __init__(self,db):
        self.apriori = Apriori()
        self.indexings = Indexing() 
        self.hashCount = dict()     #DB get Hash Count
        self.db = db
        if db['HashCount'] !=None:
            cursor = db.HashCount.find()
            for document in cursor:
                self.hashCount[document["hashStr"]] = document["count"]

         
    def Push(self, type , key):
        if type=="read" or type=="update" or type=="create":
            if any(key == hashStr for hashStr in self.hashCount.keys()):
                self.hashCount[key] += 1
                self.db.HashCount.update({"hashStr":key},{"$inc":{"count":1}})
            else:
                self.hashCount[key] = 1
                self.db.HashCount.insert({"hashStr":key,"count":1})



    def Run(self, schemaList,columnList):
        #get hashCount / get Schemas

        supportList = self.apriori.Run(self.hashCount)
        columnSupportList = dict()
        for schema in schemaList: 
            columnSupportList[schema['URL']] = []
            
        for list1 in supportList:
            columnDict = dict()
            for idx in list1:
                str =  columnList[idx]
                item =columnList[idx].split('.',1)
                URL = item[0]
                if columnDict.get(URL) == None:
                    columnDict[URL] = []
                columnDict[URL].append(item[1])

            for item in columnDict.items():
                columnSupportList[item[0]].append(item[1])
        newSchema = []
        for schema in schemaList:
            allColumn = []
            for column in schema['column']:
                allColumn.append(column)
            for childS in schema['child']:
                for column in childS['column']:
                    allColumn.append(column)

            columnCopy = allColumn.copy()
            for column in allColumn:
                for list1 in columnSupportList[schema['URL']]:
                    for column2 in list1:
                        if column==column2:
                            columnCopy.remove(column)  
                            continue
            for column in columnCopy:
                allColumn.remove(column)
            columnSupportList[schema['URL']].append(columnCopy) 
            if schema['column'] != allColumn:
                newSchema.append(self.createNewSchema(schema['URL'],columnSupportList[schema['URL']]))
         
        return newSchema

    def createNewSchemaList(self, csList):
        schemaList=[]
        for item in csList.items():
            schemaList.append(self.createNewSchema(item[0],item[1]))
        return schemaList

    def defaultSchema_copy(self):
        schema = {'URL':'', 'column':[],'child':[]}
        return schema

    def createNewSchema(self, URL,list1):
        schema = self.defaultSchema_copy()
        schema['URL']=URL
        schema['column'] = list1[0]
        for i in range(1,len(list1)):
            if len(list1[i]) == 0:
                break;
            childS = self.defaultSchema_copy()
            childS['URL'] = URL+"_"+str(i)
            childS['column'] = list1[i]
            schema['child'].append(childS) 
        return schema