class ConvertColumn:

    def __init__(self):
        # columnList db에 저장 후 가져오기
        self.columnList=[];
        #ConvertColumn.columnList.append("loc")
        #ConvertColumn.columnList.append("createdAt")
        #ConvertColumn.columnList.append("name")
        #ConvertColumn.columnList.append("subject")
        #ConvertColumn.columnList.append("content")
        #ConvertColumn.columnList.append("id")
        #ConvertColumn.columnList.append("pw")
        #ConvertColumn.columnList.append("phone")
        pass

    def columnsToIdxString(self, columns):
        return self.idxListToIdxString(self.columnsToIdxList(columns))
        
    def columnsToIdxList(self,columns):
        idxList=[];
        for key in columns:
            try:
                idx = self.columnList.index(key)
            except Exception:
                self.columnList.append(key)
                idx = self.columnList.index(key)
            idxList.append(idx) 
        idxList.sort();
        return idxList

    def idxListToIdxString(self,idxList):
        idxStringList=[]
        for idx in idxList:
            idxStringList.append(str(idx))
        idxstring = ",".join(idxStringList)
        return idxstring;


    