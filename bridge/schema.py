class Schema:
    def __init__(self, jsonSchema, db, push,depth=None):
        self.name = jsonSchema["URL"]
        self.db = db
        self.depth = 0
        if depth != None:
            self.depth = depth
        self.schemalistConnection = db['SchemaList']
        self.schemaConnect = db[self.name]
        self.push = push
        self.schemaList = []
        self.schemaValue = None
        self.setSchemaValue(jsonSchema)
        self.schemaColumnList=self.getColumnList()

    def hasColumn(self, column):
        has = False
        for c1 in self.schemaColumnList:
            if column==c1:
                has = True
                break
        return has

    def hasColumnAtAll(self, column):
        has = False
        allList = self.getAllColumnList()
        for c1 in allList:
            if column==c1:
                has = True
                break
        return has

    def hasColumnList(self, columnList):
        newList=list()
        for c1 in self.schemaColumnList:
            for c2 in columnList:
                if c1 == c2:
                    newList.append(c1)
                    break
        return newList

    def setSchemaValue(self,newSchemaValue):
        if self.schemaValue is not None: #db no change get child schema
            if self.schemaValue == newSchemaValue :
                return
            else:#Db data CHANGE
                pass

        #get child schema
        self.schemaValue = newSchemaValue
        self.schemaList.clear()
        for childS in newSchemaValue['child']:
            self.schemaList.append(Schema(childS,self.db,self.push,self.depth+1))

    def equalList(self,columnList1, columnList2):
        if len(columnList1) != len(columnList2):
            return False
        for c1 in columnList1:
            hasC = False
            for c2 in columnList2:
                if c1 == c2:
                    hasC = True
                    columnList2.remove(c2)
                    break;
            if hasC == False:
                return False
        if len(columnList2) >0:
            return False
        else:
            return True

    def find(self, param1, param2=None):
        try:
            keyList=list()
            keyList2 = list()

            if param2 != None:
                for key in param1.keys():
                    keyList.append(self.name+"."+key)
                    keyList2.append(key)
                for key in param2.keys():
                    keyList.append(self.name+"."+key)
                    keyList2.append(key)
            else:
                if self.depth !=0 :
                    raise Exception
                allList = self.getAllColumnList()
                for key in allList:
                    keyList.append(self.name+"."+key)
                    keyList2.append(key)

            if self.depth == 0 :
                self.push("read",keyList)

            if self.equalList(self.schemaColumnList,keyList2):
                if param2 is None:
                    return self.schemaConnect.find(param1)
                else:
                    return self.schemaConnect.find(param1, param2)

            for childS in self.schemaList:
                cursor = childS.find(param1, param2)
                if cursor is not None:
                    return cursor

            no_id = {"_id" : 0 }

            if self.depth == 0:
                if param2 is None:
                    return self.db[self.name+"_default"].find(param1, no_id)
                else:
                    param2["_id"] = 0
                    return self.db[self.name+"_default"].find(param1,param2)

        except Exception:
            if self.depth == 0:
                if param2 is None:
                    return self.db[self.name+"_default"].find(param1)
                else:
                    return self.db[self.name+"_default"].find(param1,param2)


    def insert(self, param1, param2=None):
        try:
            keyList=list()
            hasfKey = False
            for key in param1.keys():
                if key == "fk":
                    hasfKey = True
                    break
            for key in param1.keys():
                keyList.append(self.name+"."+key)

                if self.hasColumnAtAll(key) is False  and hasfKey is False:
                    self.schemaColumnList.append(key)
                    self.schemaValue['column'].append(key)
                    self.schemalistConnection.update({'URL':self.name} , {'$push':{'column':key}},True)

            if hasfKey==False:  #if not child schema
                self.push("create",keyList)

            currentColumnList = self.hasColumnList(param1.keys())
            if len(currentColumnList)==0 and hasfKey==True:
                return

            newParam=dict()
            for currentColumn in currentColumnList:
                newParam[currentColumn] = param1[currentColumn]
            if hasfKey==True:
                newParam['fk'] = param1['fk']
            if param2 is None:
                _id= self.schemaConnect.insert_one(newParam).inserted_id
            else:
                _id= self.schemaConnect.insert_one(newParam,param2).inserted_id

            newParam = dict()
            newParam['fk'] = _id
            for key in param1.keys():
                if self.hasColumn(key) == False:
                    newParam[key] = param1[key]
            for childS in self.schemaList:
                childS.insert(newParam, param2)
        except Exception:
            pass
        finally:
            if hasfKey == False:
                if param2 is None:
                    self.db[self.name+"_default"].insert(param1)
                else:
                    self.db[self.name+"_default"].insert(param1,param2)


    def getColumnList(self):
        columnList = []
        for column in self.schemaValue['column']:
            columnList.append(column)
        return columnList

    def getAllColumnList(self):
        allColumn = []
        for column in self.schemaValue['column']:
            allColumn.append(column)
        for childS in self.schemaValue['child']:
            for column in childS['column']:
                allColumn.append(column)
        return allColumn