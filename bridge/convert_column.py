import sys


class ConvertColumn:

    def __init__(self, columnList,db):
        self.columnList=columnList;
        self.columnlistConnect = db.ColumnList
        
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
                self.columnlistConnect.insert({'idx':idx,'column':key})
            idxList.append(idx) 
        idxList.sort();
        return idxList

    def idxListToIdxString(self,idxList):
        idxStringList=[]
        for idx in idxList:
            idxStringList.append(str(idx))
        idxstring = ",".join(idxStringList)
        return idxstring;


    