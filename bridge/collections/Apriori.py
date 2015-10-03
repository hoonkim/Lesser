import string

class Apriori:

    def __init__(self):
        self.SupportList=dict()
        
    def Run(self, HashCount, Schemas):
        self.HashCount = HashCount
        self.Schemas = Schemas
        self.SupportList.clear()

        k=1
        while(k<5):
            MakeKSupportList(k)
        #hashCount to SupportList K
        #while k<5

    def MakeKSupportList(self, k):
        for keys in self.HashCount.keys():
            pass    

    #if itemset1 has itemset2  : return true   else return false
    def Compare(self,itemsetString1, itemsetString2):
        list1 = itemsetString1.split(',')
        list2 = itemsetString2.split(',')
        hasCount = 0
        for i in list1:
            for j in list2:
                if(i==j):
                    hasCount = hasCount +1 
                    continue
        if(hasCount == list2.size()):
            return True
        else:
            return False

    def HasItemset(self, itemsetString):
        index =0
        for key in self.HashCount:
            index = index+1
            Compare(key,itemsetString)

