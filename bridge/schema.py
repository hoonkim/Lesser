class Schema:
    def __init__(self, jsonSchema, db, push):
        self.name = jsonSchema["URL"]
        self.schemalistConnection = db['SchemaList']
        self.schemaConnect = db[self.name]
        self.push = push 
        self.schemaValue = jsonSchema 
        self.schemaColumnList=self.allColumnList()

    def find(self, query):
        keyList=list()
        for key in query.keys():
            keyList.append(self.name+"."+key)
        self.push("read",keyList)
        #change Query fit schemaValue
        return self.schemaConnect.find_one(query)

    def insert(self, query):
        keyList=list()
        for key in query.keys():
            keyList.append(self.name+"."+key)
            noColumn = True
            for column in self.schemaColumnList:
                if key==column:
                    noColumn = False
                    break

            if noColumn == True:
                self.schemaColumnList.append(key)
                self.schemaValue['column'].append(key)
                self.schemalistConnection.update({'URL':self.name} , {'$push':{'column':key}},True)
        self.push("create",keyList)

        return self.schemaConnect.insert_one(query)

    def allColumnList(self):
        allColumn = []
        for column in self.schemaValue['column']:
            allColumn.append(column)
        for childS in self.schemaValue['child']:
            for column in childS['column']:
                allColumn.append(column)
        return allColumn