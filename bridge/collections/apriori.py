import string
from itertools import combinations

class Apriori:

    def __init__(self):
        self.SupportList=dict()
        
    def Run(self, HashCount):
        self.HashCount = HashCount
        sumHashCount = sum(self.HashCount.values())
        k=1
        beforeSupport = dict()
        while True:
            beforeSupport = self.SupportList.copy()
            self.SupportList.clear()
            self.makeKSupportList(k)
            isBreak = False

            for item in self.SupportList.items():
                if float(item[1])/sumHashCount > 0.3:
                    isBreak = True 

            if isBreak == False or len(self.SupportList) <= 1:
                break;
            k+=1
        support=list()
        for item in beforeSupport.items():
            if float(item[1])/sumHashCount > 0.2:
                supp =list(map(int, item[0].split(',') ))
                isOverlab = False
                for i in range(0,len(support)):
                    if self.listOverlap(supp,support[i]) == True:
                        isOverlab = True
                        support[i] = list(set(supp+support[i])) 
                if isOverlab == False:
                    support.append(supp)
        return support

    
    def listOverlap(self,list1, list2):
        for item in list1:
            for item2 in list2:
                if item == item2:
                    return True
        return False

    def makeKSupportList(self, k):
        for keys in self.HashCount.keys():
            keyList = keys.split(',')
            keyCombo = list(map(','.join,combinations(keyList,k)))
            for key in keyCombo:
                if any(key in supportHash for supportHash in self.SupportList.keys()):
                    self.SupportList[key] += self.HashCount[keys]
                else:
                    self.SupportList[key] = self.HashCount[keys] 

    #if itemset1 has itemset2  : return true   else return false
    def compare(self,itemsetString1, itemsetString2):
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

    def hasItemset(self, itemsetString):
        index =0
        for key in self.HashCount:
            index = index+1
            self.compare(key,itemsetString)
            
    def powerset(self,items,size):
        combo = []
        combo.append(list(combinations(items,size)))
        return combo