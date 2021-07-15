from modAnalysis import *
from mod import Mod
from copy import deepcopy

class ModSimulation():
    
    def walkIt(self,settings):
           
        self.totalProbability=0
        self.branchCount=0

        self.modSet=settings["general"]["modSet"]

        self.analysis=ModAnalysis()
        newMod=Mod()

        newMod.pips="undefined"
        newMod.level=1
        newMod.grade="undefined"
        newMod.shape="undefined"
        newMod.primary="undefined"
        newMod.secondary={}
        
        self.settings=settings
        
        levelProbability=1
        self.energyChange(levelProbability, -16)
        self.creditChange(levelProbability, 7500)
        
        self.quickPrimaryForking=1
        self.quickSecondaryForking=1
        self.quickSpeedForking=1

        self.quickPrimaryForking=self.settings["general"]["quickPrimaryForking"]
        self.quickSecondaryForking=self.settings["general"]["quickSecondaryForking"]
        self.quickSpeedForking=self.settings["general"]["quickSpeedForking"]

        self.testlevel=0
        self.testPrintLevel=0
        self.walkPips(levelProbability,newMod)
        
        print()
        print("total probability encountered", self.totalProbability)
        print("total recursion branches", self.branchCount)
        
        return self.analysis
    
    def walkBoughtMod(self, levelProbability, mod:Mod):
        assert(mod.pips==5)
        assert(mod.shape!="arrow")
        assert(mod.shape in Mod.shapes)
        assert(mod.grade=="a")
        assert(mod.primary in mod.primaries[mod.shape])
        assert("speed" in mod.secondary)
        assert(mod.secondary["speed"][0]==1)
        assert(mod.secondary["speed"][1] in [3,4,5])
        assert(mod.level==1)
        
        self.walkSecondaryStep1(levelProbability, mod)
        pass

    def energyChange(self, levelProbability, change):
        self.analysis.avgEnergyChange+=levelProbability*change

    def creditChange(self, levelProbability, change):
        self.analysis.avgCreditsChange+=levelProbability*change

    def walkEND(self,probability):
        self.totalProbability+=probability
        self.branchCount+=1
        if (self.branchCount % 1000) == 0:
            print(".", end = "")

    def walkPips(self,levelProbability, mod:Mod):
        #newMod=deepcopy(mod)
        newMod=self.copyMod(mod)

        for pips in Mod.pipsProbability:
            if Mod.pipsProbability[pips]!=0:
                if pips==5:
                    newMod.pips=pips
                    self.walkShapes(Mod.pipsProbability[pips]/100*levelProbability, newMod)
                else:
                    #sell all less than 5 pips
                    self.creditChange(Mod.pipsProbability[pips]/100*levelProbability, Mod.modSellingPrice[pips][1])
                    self.walkEND(Mod.pipsProbability[pips]/100*levelProbability)
            
    def walkShapes(self,levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        for shape in Mod.shapeProbability:
            if self.testlevel>0:
                print("|", shape, "|", end="")
            if Mod.shapeProbability[shape]!=0:
                newMod.shape=shape
                self.walkGrades(Mod.shapeProbability[shape]/100*levelProbability, newMod)

    def walkGrades(self, levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        for grade in Mod.gradeProbability:
            if self.testlevel>1:
                print("|", grade, "|", end="")
            if Mod.gradeProbability[grade]!=0:
                newMod.grade=grade
                self.walkPrimaries(Mod.gradeProbability[grade]/100*levelProbability, newMod)
                
    def walkPrimaries(self, levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        possiblePrimaries=Mod.primariesProbability[newMod.shape]
        possiblePrimariesCount=len(possiblePrimaries.keys())

        if (self.quickPrimaryForking>0) and (newMod.shape in ["circle", "cross", "triangle"]):
            if newMod.shape in ["circle", "cross"]:
                #process only first primary on list
                #pick any primary from list of possible primaries
                for primary in possiblePrimaries:
                    newMod.primary=primary          
                if self.testlevel>2:
                    print("|", primary, "|", end="")      
                self.walkSecondaryStep1(levelProbability, newMod)
            
            else:
                assert(newMod.shape=="triangle")
                assert("crit dmg" in possiblePrimaries)
                #pick any primary but not crit dmg
                for primary in possiblePrimaries:
                    if primary!="crit dmg":
                        newMod.primary=primary
                assert(newMod.primary!="crit dmg")
                if self.testlevel>2:
                    print("|", primary, "|", end="")
                self.walkSecondaryStep1(levelProbability*(possiblePrimariesCount-1)/possiblePrimariesCount, newMod)

                #process crit dmg triangle separately
                primary="crit dmg"
                if self.testlevel>2:
                    print("|", primary, "|", end="")
                newMod.primary=primary
                self.walkSecondaryStep1(levelProbability/possiblePrimariesCount, newMod)
        
        else:
            for primary in possiblePrimaries:
                if self.testlevel>2:
                    print("|", primary, "|", end="")
                newMod.primary=primary                
                if newMod.shape!="arrow":
                    if self.testlevel>=111:
                        newMod.secondary={}
                        newMod.level=1
                       
                        if self.testPrintLevel==111:
                            self.printModChance(levelProbability, newMod)
                        self.walkEND(levelProbability/possiblePrimariesCount)
                    else:
                        self.walkSecondaryStep1(levelProbability/possiblePrimariesCount, newMod)
                else:
                    #arrow sell conditions, sell all accuracy, maybe others
                    if (newMod.primary=="accuracy") and (self.settings["general"]["sellAccuracyArrows"]==1):
                        self.creditChange(levelProbability/possiblePrimariesCount, Mod.modSellingPrice[newMod.pips][1])
                    if (newMod.primary=="speed") and (self.settings["general"]["keepSpeedArrows"]==1):
                        
                        self.analysis.analyzeMod(levelProbability/possiblePrimariesCount, newMod)
                    self.walkEND(levelProbability/possiblePrimariesCount)

    def walkSecondaryStep1(self, levelProbability, mod:Mod):
        newMod=mod

        if (self.settings["minInitialSpeed"][newMod.grade][newMod.shape]==6):
            self.creditChange(levelProbability, Mod.modSellingPrice[newMod.pips][newMod.level])
            self.walkEND(levelProbability)
        else:
            self.walkInitialSecondaryStats(levelProbability, newMod)

    def walkAddNewSecondaryStat(self, levelProbability, mod:Mod, recursionReturnFunction):
        newMod=self.copyMod(mod)
        possibleStats=[]
        for stat in Mod.secondaries:
            if ( stat!=newMod.primary ) and ( stat not in newMod.secondary ):
                possibleStats.append(stat)            
        possibleStatsCount=len(possibleStats)

        tmpBool=True
        tmpBool=tmpBool and (self.quickSpeedForking and "speed" not in newMod.secondary and (self.settings["minInitialSpeed"][newMod.grade][newMod.shape] not in [4,5]))
        tmpBool=tmpBool and not (self.settings["general"]["greyMaxInitialStats"]<4 and newMod.grade=="e")
        if tmpBool:
            #put speed as first secondary with probability of mod having speed
            #speedChance=4/possibleStatsCount
            newMod.secondary["speed"]=[1,0]
            for speed in Mod.initialSpeedProbability:
                if Mod.initialSpeedProbability[speed]!=0:
                    newMod.secondary["speed"][1]=speed
                    recursionReturnFunction(levelProbability * Mod.initialSpeedProbability[speed]/100/possibleStatsCount * 4, newMod)

            # create proper mod that has 4 stats that are not speed, with remainder of probability
            newMod=self.copyMod(mod)
            assert(newMod.level==1 or newMod.level==3) 
            initialStatCount={"a":4, "b":3, "c":2, "d":1, "e":0}[newMod.grade]   
            while newMod.getSecondaryStatCount() < initialStatCount:
                assert(possibleStats[newMod.getSecondaryStatCount()] !="speed")
                newMod.secondary[possibleStats[newMod.getSecondaryStatCount()]]=1

            if newMod.level==3 and newMod.getSecondaryStatCount() < initialStatCount+1:
                newMod.secondary[possibleStats[newMod.getSecondaryStatCount()]]=1

            while newMod.getSecondaryStatCount() < 4:
                assert(possibleStats[newMod.getSecondaryStatCount()] !="speed")
                newMod.secondary[possibleStats[newMod.getSecondaryStatCount()]]=1

                if newMod.level==1:
                    cost=Mod.modLevelingCost[newMod.pips][1]+Mod.modLevelingCost[newMod.pips][2]
                    self.creditChange(levelProbability * (1 - 4/possibleStatsCount), -cost)
                    newMod.level=3
                else:
                    cost=0
                    for x in range (0,3):
                        cost+=Mod.modLevelingCost[newMod.pips][newMod.level+x]
                    self.creditChange(levelProbability * (1 - 4/possibleStatsCount), -cost)
                    newMod.level+=3
            assert (newMod.getSecondaryStatCount()==4)
            recursionReturnFunction(levelProbability * (1 - 4/possibleStatsCount), newMod)

        else:
            if self.quickSecondaryForking>0:                
                assert(possibleStats[0]!="speed")
                if "speed" not in possibleStats:
                    newMod=self.copyMod(mod)
                    newMod.secondary[possibleStats[0]]=1
                    recursionReturnFunction(levelProbability*1, newMod)

                else:
                    newMod=self.copyMod(mod)
                    newMod.secondary[possibleStats[0]]=1 # first possible stat, distribution remains same so multiply weight
                    assert(possibleStatsCount>1)
                    recursionReturnFunction(levelProbability/possibleStatsCount*(possibleStatsCount-1), newMod)

                    newMod=self.copyMod(mod)
                    newMod.secondary["speed"]=[1,0]
                    for speed in Mod.initialSpeedProbability:
                        if Mod.initialSpeedProbability[speed]!=0:
                            newMod.secondary["speed"][1]=speed
                            recursionReturnFunction(levelProbability * Mod.initialSpeedProbability[speed]/100/possibleStatsCount, newMod)

            else:
                for stat in possibleStats:
                    newMod=self.copyMod(mod)
                    if stat != "speed":
                        newMod.secondary[stat]=1
                        recursionReturnFunction(levelProbability/possibleStatsCount, newMod)
                    else:
                        newMod.secondary[stat]=[1,0]
                        for speed in Mod.initialSpeedProbability:
                            if Mod.initialSpeedProbability[speed]!=0:
                                newMod.secondary["speed"][1]=speed
                                recursionReturnFunction(levelProbability*Mod.initialSpeedProbability[speed]/100/possibleStatsCount, newMod)

    def walkInitialSecondaryStats(self, levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        initialStatCount={"a":4, "b":3, "c":2, "d":1, "e":0}[newMod.grade]     

        if newMod.getSecondaryStatCount() < initialStatCount:
            self.walkAddNewSecondaryStat(levelProbability, newMod, self.walkInitialSecondaryStats)
        else:
            #self.printModChance(levelProbability, newMod)
            assert(newMod.getSecondaryStatCount()=={"a":4, "b":3, "c":2, "d":1, "e":0}[newMod.grade] or self.quickSpeedForking)  
            # end of walkSecondaryStep1 recursion
            if self.testlevel>=110:
                if self.testPrintLevel==110:
                    self.printModChance(levelProbability, newMod)
                self.walkEND(levelProbability)
               # print(levelProbability)
            else:
                self.walkLevelUpUntilSpeed(levelProbability, newMod)
     
    def walkLevelUpUntilSpeedStep1(self, levelProbability, mod:Mod):
        #newMod=self.copyMod(mod)
        #no changes in this procedure
        newMod=mod 

        #sell all given grade?
        if (self.settings["minInitialSpeed"][newMod.grade][newMod.shape]==6):
            self.creditChange(levelProbability, Mod.modSellingPrice[newMod.pips][newMod.level])
            self.walkEND(levelProbability)
        else:
            self.walkLevelUpUntilSpeed(levelProbability, newMod)

    def walkLevelUpUntilSpeed(self, levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        tmpBool=True
        tmpBool=tmpBool and ("speed" not in newMod.secondary)
        tmpBool=tmpBool and (newMod.level < 12)
        tmpBool=tmpBool and (newMod.getSecondaryStatCount()<4)
        tmpBool=tmpBool and (newMod.grade!="e" or (newMod.getSecondaryStatCount() < self.settings["general"]["greyMaxInitialStats"]))
        if tmpBool:
            ## No speed yet, and less than 4 secondary stats
            if newMod.level==1:
                cost=Mod.modLevelingCost[newMod.pips][1]+Mod.modLevelingCost[newMod.pips][2]
                self.creditChange(levelProbability, -cost)
                newMod.level=3
            else:
                cost=0
                for x in range (0,3):
                    cost+=Mod.modLevelingCost[newMod.pips][newMod.level+x]
                self.creditChange(levelProbability, -cost)
                newMod.level+=3
            assert(newMod.getSecondaryStatCount()<4)
            self.walkAddNewSecondaryStat(levelProbability, newMod, self.walkLevelUpUntilSpeed)
        else:
            if ("speed" not in newMod.secondary):
                if self.settings["general"]["sellNoSpeedMods"]==1:
                    #sell all no speeeds
                    self.creditChange(levelProbability, Mod.modSellingPrice[newMod.pips][newMod.level])
                    self.walkEND(levelProbability)
                else:
                    self.analysis.analyzeMod(levelProbability, newMod)
                    self.walkEND(levelProbability)
            else:
                if self.testlevel>=109:
                    if self.testPrintLevel==109:
                        self.printModChance(levelProbability, newMod)
                    self.walkEND(levelProbability)
                self.walkGotSpeed(levelProbability, newMod)

    def walkGotSpeed(self, levelProbability, mod:Mod):
        #newMod=self.copyMod(mod)
        #no changes to object
        newMod=mod

        assert("speed" in newMod.secondary)
        #decide if keep mod now
  
        if (self.settings["minInitialSpeed"][newMod.grade][newMod.shape] > newMod.secondary["speed"][1]):
            #mod does not meet minimum speed criteria
            if self.settings["general"]["sellTooLowInitialSpeedMods"]==1:
                #sell too low speed
                self.creditChange(levelProbability, Mod.modSellingPrice[newMod.pips][newMod.level])
                self.walkEND(levelProbability)
            else:
                print(newMod.secndary["speed"])
                self.analysis.analyzeMod(levelProbability, newMod)
                self.walkEND(levelProbability)
        else:
            self.walkLevelUpTo12(levelProbability, newMod)

    def walkLevelUpTo12(self,levelProbability, mod:Mod):
        newMod=self.copyMod(mod)
        if (newMod.level < 12):
            ## OOkay, level up time
            if newMod.level==1:
                cost=Mod.modLevelingCost[newMod.pips][1]+Mod.modLevelingCost[newMod.pips][2]
                self.creditChange(levelProbability, -cost)
                newMod.level=3
            else:
                cost=0
                for x in range (0,3):
                    cost+=Mod.modLevelingCost[newMod.pips][newMod.level+x]
                self.creditChange(levelProbability, -cost)
                newMod.level+=3

            if newMod.getSecondaryStatCount() < 4:
                self.walkAddNewSecondaryStat(levelProbability, newMod, self.walkLevelUpTo12)
            else: 
                self.walkIncreaseExistingStat(levelProbability, newMod, self.walkLevelUpTo12)

        else:
            assert(newMod.level==12)
            if self.testlevel>=108:
                if self.testPrintLevel==108:
                    self.printModChance(levelProbability, newMod)
                self.walkEND(levelProbability)
            else:
                self.walkSliceUpStep1(levelProbability, newMod)

    def walkSliceUpStep1(self, levelProbability, mod:Mod):
        #newMod=self.copyMod(mod)
        #no changes!
        newMod=mod

        #decision point
        isMinLev12Speed=(self.settings["minLev12Speed"][newMod.grade][newMod.shape] <= newMod.secondary["speed"][1])

        if isMinLev12Speed:
            self.walkSliceUp(levelProbability, newMod)
        else:
            self.analysis.analyzeMod(levelProbability ,newMod)
            self.walkEND(levelProbability)
    
    def walkIncreaseExistingStat(self, levelProbability, mod:Mod, recursionReturnFunction):
        newMod=self.copyMod(mod)
        if self.quickSecondaryForking>0:
            assert("speed" in newMod.secondary)
            ## find a stat that is not speed and increase it
            for stat in newMod.secondary:
                if stat!="speed":
                    statNotSpeed=stat
            assert(statNotSpeed!="speed")

            newMod.secondary[statNotSpeed]+=1
            recursionReturnFunction(levelProbability*3/4, newMod)

            for speed in Mod.increaseSpeedProbability:
                newMod=self.copyMod(mod)
                if Mod.increaseSpeedProbability[speed]!=0:
                    newMod.secondary["speed"][0]+=1
                    newMod.secondary["speed"][1]+=speed
                    recursionReturnFunction(levelProbability/4*Mod.increaseSpeedProbability[speed]/100, newMod)
            
        else:                
            for stat in newMod.secondary:
                newMod=self.copyMod(mod)
                if stat!="speed":
                    newMod.secondary[stat]+=1
                    recursionReturnFunction(levelProbability/4, newMod)
                else:
                    for speed in Mod.increaseSpeedProbability:
                        newMod=self.copyMod(mod)

                        if Mod.increaseSpeedProbability[speed]!=0:
                            newMod.secondary["speed"][0]+=1
                            newMod.secondary["speed"][1]+=speed
                            recursionReturnFunction(levelProbability/4*Mod.increaseSpeedProbability[speed]/100, newMod)

    def walkSliceUp(self,levelProbability, mod:Mod):
        newMod=self.copyMod(mod)

        isSpeedBumpMissed=(newMod.getSecondaryStatIncreaseCount() != newMod.secondary["speed"][0] -1)
        isMissAllowed=(self.settings["minSpeedIfBumpMissed"][newMod.grade][newMod.shape]!=0)
        isMinSpeedOnMiss=(self.settings["minSpeedIfBumpMissed"][newMod.grade][newMod.shape]<=newMod.secondary["speed"][1])
        isMaxGrade=(newMod.grade=="a")

        shouldSlice=(not isSpeedBumpMissed)
        shouldSlice=shouldSlice or (isMissAllowed and isMinSpeedOnMiss)
        shouldSlice=shouldSlice and not isMaxGrade        
        if (shouldSlice) :
            assert(newMod.level==12 or newMod.level==15)
            if newMod.level==12:
                cost=0
                for x in range (0,3):
                    cost+=Mod.modLevelingCost[newMod.pips][newMod.level+x]
                self.creditChange(levelProbability, -cost)
                newMod.level+=3

            assert(newMod.level==15)
            cost=Mod.modSlicingCost[newMod.grade]
            self.creditChange(levelProbability, -cost["credits"])
            #average 1.2material per 12 energy
            self.energyChange(levelProbability, -cost["mats"]*10)
            self.creditChange(levelProbability, cost["mats"]*1000) # 1200 credits income for 12 energy for 1.2 mat income from mat roll!
            newMod.grade=Mod.grades[Mod.grades.index(newMod.grade)+1]
            
            self.walkIncreaseExistingStat(levelProbability, newMod, self.walkSliceUp)

            # #increase stat
            # if self.quickSecondaryForking>0:
            #     newSecondary=self.copySecondary(secondary)
            #     ## find a stat that is not speed and increase it
            #     for stat in newSecondary:
            #         if stat!="speed":
            #             statNotSpeed=stat
            #     assert(statNotSpeed!="speed")
            #     newSecondary[statNotSpeed]+=1
            #     self.walkSliceUp(levelProbability*3/4, grade, level, newSecondary)
            #     newSecondary=self.copySecondary(secondary)
            #     for speed in Mod.increaseSpeedProbability:
            #         newestSecondary=self.copySecondary(newSecondary)
            #         if Mod.increaseSpeedProbability[speed]!=0:
            #             newestSecondary["speed"][0]+=1
            #             newestSecondary["speed"][1]+=speed
            #             self.walkSliceUp(levelProbability/4*Mod.increaseSpeedProbability[speed]/100, grade, level, newestSecondary)

            # else:
            #     for stat in secondary:
            #         newSecondary=self.copySecondary(secondary)
            #         if stat!="speed":
            #             newSecondary[stat]+=1
            #             self.walkSliceUp(levelProbability/4, grade, level, newSecondary)
            #         else:
            #             for speed in Mod.increaseSpeedProbability:
            #                 newestSecondary=self.copySecondary(newSecondary)
            #                 if Mod.increaseSpeedProbability[speed]!=0:
            #                     newestSecondary["speed"][0]+=1
            #                     newestSecondary["speed"][1]+=speed
            #                     self.walkSliceUp(levelProbability/4*Mod.increaseSpeedProbability[speed]/100, grade, level, newestSecondary)

        else:
            if self.testlevel>=107:
                if self.testPrintLevel==107:
                    self.printModChance(levelProbability, newMod)
                self.walkEND(levelProbability)
            self.analysis.analyzeMod(levelProbability, newMod)
            self.walkEND(levelProbability)
            
    def getSecondaryStatIncreaseCount(self,secondary):
        count=0
        for stat in secondary:
            if stat!="speed":
                count+=secondary[stat]
            else:
                count+=secondary[stat][0]
        return count

    def printModChance(self, probability, mod):
        print("pips:", mod.pips, "grade:",mod.grade, "shape:",mod.shape, "primary:",mod.primary,"level:",mod.level, "secondary:",mod.secondary, "chance:",probability)
 
    def copyMod(self, mod:Mod):
        newMod=Mod()
        newMod.modSet=mod.modSet
        newMod.level=mod.level
        newMod.grade=mod.grade
        newMod.shape=mod.shape
        newMod.pips=mod.pips
        newMod.primary=mod.primary
        newMod.secondary={}
        for stat in mod.secondary:
            if stat!="speed":
                newMod.secondary[stat]=mod.secondary[stat]
            else:
                newMod.secondary["speed"]=[mod.secondary["speed"][0],mod.secondary["speed"][1]]
        return newMod
        
    def copySecondary(self,secondary):
        newSecondary={}
        for statCopy in secondary:
            if statCopy!="speed":
                newSecondary[statCopy]=secondary[statCopy]
            else:
                newSecondary[statCopy]=[secondary[statCopy][0],secondary[statCopy][1]]
        return newSecondary

   
