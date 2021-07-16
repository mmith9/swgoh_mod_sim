
from pandas_ods_reader import read_ods

from mod import Mod

class ModStore:
    
    def __init__(self):

        self.testlevel=0

        odsFileName="mod_store_inventory.ods"
        odsData=read_ods(odsFileName,1)

        self.storeModCount=len(odsData["shop:shape"])
        self.storeModList=[]
        for x in range(0, self.storeModCount):
            mod={"shape":odsData["shop:shape"][x], "grade":odsData["shop:grade"][x], "modSet":odsData["shop:modset"][x],
                  "primary":odsData["shop:primary"][x], "secondarySpeed":odsData["shop:secondary_speed"][x], "currency":odsData["shop:currency"][x]}
            self.storeModList.append(mod)

        for x in range(0, self.storeModCount):
            if self.storeModList[x]["modSet"]=="cc":
                self.storeModList[x]["modSet"]="crit chance"
            if self.storeModList[x]["modSet"]=="cd":
                self.storeModList[x]["modSet"]="crit dmg"
            if self.storeModList[x]["modSet"]=="hp":
                self.storeModList[x]["modSet"]="health %"
            if self.storeModList[x]["modSet"]=="def":
                self.storeModList[x]["modSet"]="defense %"
            if self.storeModList[x]["modSet"]=="off":
                self.storeModList[x]["modSet"]="offense %"
        
        circleCount=0
        for x in range(0, self.storeModCount):
            if self.storeModList[x]["primary"]=="cc":
                self.storeModList[x]["primary"]="crit chance"
            if self.storeModList[x]["primary"]=="cd":
                self.storeModList[x]["primary"]="crit dmg"
            if self.storeModList[x]["primary"]=="hp":
                self.storeModList[x]["primary"]="health %"
            if self.storeModList[x]["primary"]=="prot":
                self.storeModList[x]["primary"]="protection %"
            if self.storeModList[x]["primary"]=="ca":
                self.storeModList[x]["primary"]="crit avoidance"
            if self.storeModList[x]["primary"]=="off":
                self.storeModList[x]["primary"]="offense %"
            if self.storeModList[x]["primary"]=="def":
                self.storeModList[x]["primary"]="defense %"
            if self.storeModList[x]["primary"]=="acc":
                self.storeModList[x]["primary"]="accuracy"

            if self.storeModList[x]["shape"]=="square":
                self.storeModList[x]["primary"]="offense %"
            if self.storeModList[x]["shape"]=="diamond":
                self.storeModList[x]["primary"]="defense %"
            
            if self.storeModList[x]["shape"]=="circle":
                circleCount+=1
                if (circleCount % 2):
                    self.storeModList[x]["primary"]="health %"
                else:
                    self.storeModList[x]["primary"]="protection %"

            if self.storeModList[x]["currency"]!="ship":
                self.storeModList[x]["currency"]="credits"
            
    def getModChance(self, mod:Mod, currency="credits"):
        assert(self.storeModCount>0)

        modInListCount=0
        for x in range(0,self.storeModCount):
            tmpBoolean=True
            tmpBoolean=tmpBoolean and self.storeModList[x]["shape"] == mod.shape
            tmpBoolean=tmpBoolean and self.storeModList[x]["grade"] == mod.grade
            tmpBoolean=tmpBoolean and self.storeModList[x]["modSet"] == mod.modSet
            tmpBoolean=tmpBoolean and self.storeModList[x]["primary"] == mod.primary
            tmpBoolean=tmpBoolean and self.storeModList[x]["currency"] == currency
            tmpBoolean=tmpBoolean and self.storeModList[x]["secondarySpeed"] == mod.secondary["speed"][1]
            if tmpBoolean:
                modInListCount+=1
        
        return modInListCount/self.storeModCount

    def getModPrice(self, currency="credits"):
        level15modCost={"credits": 4158400, "ship":1910000}
        return level15modCost[currency]

    def modShopping(self, budget, wishList, currency="credits"):
        stuffBought=[]
        for item in wishList:
            if self.testlevel>1 :
                print(item)
            itemExpanded=[]
            self.expandItemToItems(item, itemExpanded)
        
        ##


        mod=Mod()
        mod.pips=5
        mod.shape="triangle"
        mod.grade="a"
        mod.primary="crit dmg"
        mod.level=1
        mod.secondary["speed"]=[1,5]
        probability=0.316464390792661
        price=self.getModPrice()
        canAfford=1
        if price*probability>budget:
            canAfford=budget/(price*probability)
        
        price=price-86200
        item={"mod":mod, "dailyCreditCost":price*probability*canAfford, "dailyProbability":probability*canAfford}
        stuffBought=[item]
        return stuffBought
    #TODO 

    def expandItemToItems(self, item, itemExpanded):
        if self.testlevel>1:
            print("item",item)
        if item["shape"]=="any":
            for shape in Mod.shapes:
                self.expandItemToItemsGrade(item, itemExpanded, shape)
        elif item["shape"]=="not arrow":
            for shape in Mod.shapes:
                if shape!="arrow":
                    self.expandItemToItemsGrade(item, itemExpanded, shape)
        else:
            self.expandItemToItemsGrade(item, itemExpanded, item["shape"])
    
    def expandItemToItemsGrade(self, item, itemExpanded, shape):
        if item["grade"]=="any":
            for grade in Mod.grades:
                self.expandItemToItemsModSet(item, itemExpanded, shape, grade)
        else:
            self.expandItemToItemsModSet(item, itemExpanded, shape, item["grade"])

    def expandItemToItemsModSet(self, item, itemExpanded, shape, grade):
        if item["modSet"]=="any":
            for modSet in Mod.modSets:
                self.expandItemToItemsPrimary(item, itemExpanded, shape, grade, modSet)
        else:
            self.expandItemToItemsPrimary(item, itemExpanded, shape, grade, item["modSet"])

    def expandItemToItemsPrimary(self, item, itemExpanded, shape, grade, modSet):
        if item["primary"]=="any":
            for primary in Mod.primaries[shape]:
                self.expandItemToItemsSpeed(item, itemExpanded, shape, grade, modSet, primary)
        else:
            self.expandItemToItemsSpeed(item, itemExpanded, shape, grade, modSet, item["primary"])
    
    def expandItemToItemsSpeed(self, item, itemExpanded, shape, grade, modSet, primary):
        if item["speed"]=="any":
            for speed in [3,4,5]:
                self.expandItemToItemsLastStep(item, itemExpanded, shape, grade, modSet, primary, speed)
        else:
            self.expandItemToItemsLastStep(item, itemExpanded, shape, grade, modSet, primary, item["speed"])
    
    def expandItemToItemsLastStep(self, item, itemExpanded, shape, grade, modSet, primary, speed):
        tmp={}
        tmp["shape"]=shape
        tmp["grade"]=grade
        tmp["modSet"]=modSet
        tmp["primary"]=primary
        tmp["speed"]=speed
        itemExpanded.append(tmp)
        #print(tmp)

        

