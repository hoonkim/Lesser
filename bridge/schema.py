class Schema:
    def __init__(self, jsonSchema, db, push):
        self.name = jsonSchema["URL"]
        self.db = db
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
            self.schemaList.append(Schema(childS,self.db,self.push))


        #현재 스키마와 다르면 DB Data change!!!

        #allColumnList를 뺴고 현재 schemaValue의 칼럼리스트를 가지고있으면됨
        #find / insert 할 때 self.push함수 호출시 중복되지 않도록 주의
        #find / insert 할 때 schema의 자식들을 돌며 columnList 일치시 쿼리를 날림
        #스키마가 분할되어 있을 시 find의 경우 루트스키마의 _id값을 알아낸 후 자식스키마의 fk로 find, 결과는 merge하면됨
        #스키마가 분할되어 있을 시 insert는 내일 생각하고 잠자자

#조건 / 찾는 column이 한 스키마 내인경우 그냥 쓰면 됨
#조건이 부모 / 찾는 column이 자식 스키마 인 경우
#조건이 자식 / 찾는 column이 부모 스키마인 경우
    def find(self, param1, param2=None):
        keyList=list()
        for key in param1.keys():
            keyList.append(self.name+"."+key)
        self.push("read",keyList)
        #change Query fit schemaValue
        if param2 is None:
            return self.schemaConnect.find_one(param1)
        else:
            return self.schemaConnect.find_one(param1, param2)

    def insert(self, param1, param2=None):
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