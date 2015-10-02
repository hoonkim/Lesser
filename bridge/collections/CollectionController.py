from Collections.Apriori import Apriori
from Collections.Indexings import Indexing
import pymongo

class CollectionController:

    def __init__(self,db):
        self.apriori = Apriori()
        self.indexings = Indexing() 
        self.hashCount = dict()     #DB get Hash Count
        cursor = db.hashCount.find()
        for document in cursor:
            self.hashCount[document["hashStr"]] = document["count"]
         
    def Push(self, key , type):
        if type=="read" or type=="update":
            if any(key in hashStr for hashStr in self.hashCount.keys()):
                self.hashCount[key] += 1
                self.db.hashCount.update({"hashStr":key},{"$inc":{"count":1}})
            else:
                self.hashCount[key] = 1
                self.db.hashCount.insert({"hashStr":key,"count":1})



    def Run(self, schemaList):
        #get hashCount / get Schemas
        self.schemaList = schemaList

        self.apriori.Run(self.hashCount, schemaList)




        #set hashCount / set Schemas
        return newSchema
