class Schema:
    def __init__(self, name, db, push):
        self.name = name
        self.schemaConnect = db[name]
        self.push = push 
        self.schemaValue = {'url':name,'column':[],'child':[]}
        cursor = db['SchemaList'].find({'url':name})
        for document in cursor:
            print(document)


    def find(self, query):
        self.push("read",["id","pw"])
        #change Query fit schemaValue
        pass

    def insert(self, query):
        #self.push(keys)
        self.push("create",["id","pw","phone"])
        #change Query fit schemaValue
        #if new key in query : update SchemaValue , update DB Schema Value
        pass