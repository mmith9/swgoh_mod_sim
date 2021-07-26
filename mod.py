import random


class Mod:

    
    def __init__(self):
        self.modSet=""
        self.level=0
        self.grade=""
        self.shape=""
        self.pips=0
        self.primary=""
        self.secondary={}
 
    def rollNew(self,modSet):
        self.modSet=modSet
        self.level=1
        self.grade=Mod.getRndFromDistribution(Mod.gradeProbability)
        self.shape=Mod.getRndFromDistribution(Mod.shapeProbability)
        self.pips=Mod.getRndFromDistribution(Mod.pipsProbability)
        self.primary=Mod.getRndFromDistribution(Mod.primariesProbability[self.shape])
        self.secondary={}
        if (self.grade=="a"):
            self.addNewStat()
            self.addNewStat()
            self.addNewStat()
            self.addNewStat()
        if (self.grade=="b"):
            self.addNewStat()
            self.addNewStat()
            self.addNewStat()
        if (self.grade=="c"):
            self.addNewStat()
            self.addNewStat()
        if (self.grade=="d"):
            self.addNewStat()
            
    def setStats(self,level,grade,shape,modSet,pips,primary,secondary):
        self.level=level
        self.grade=grade
        self.shape=shape
        self.modSet=modSet
        self.pips=pips
        self.primary=primary
        self.secondary=secondary

    def addNewStat(self):
        possibleStats=[]
        for stat in Mod.secondaries:
            possibleStats.append(stat)
        #print(possibleStats)
        if self.primary in possibleStats:
            possibleStats.remove(self.primary)
        for existingStat in self.secondary:
            #existingStatName=list(existingStat.keys())[0]
            if existingStat in possibleStats:
                possibleStats.remove(existingStat)
        #print(possibleStats)
        possibleStatsProbability={}
        for stat in possibleStats:
            possibleStatsProbability[stat]=Mod.secondariesProbability[stat]
        newStat=Mod.getRndFromDistribution(possibleStatsProbability)
        if newStat=="speed":
            newSpeed=Mod.getRndFromDistribution(Mod.initialSpeedProbability)
            self.secondary[newStat]=[1,newSpeed]
        else:
            self.secondary[newStat]=[1,0]

    def increaseExistingStat(self):
        whichStat=random.randint(0,3)
        #print(whichStat)
        statName=list(self.secondary.keys())[whichStat]
        #print(statName)
        self.secondary[statName][0]+=1
        if statName=="speed":
            increase=Mod.getRndFromDistribution(Mod.increaseSpeedProbability)
            self.secondary[statName][1]+=increase

    def levelUp(self):
        cost={}
        cost["credits"]=Mod.modLevelingCost[self.pips][self.level]
        self.level+=1
        if ((self.level % 3) == 0) and (self.level<15):
            if (len(self.secondary)<4):
                self.addNewStat()
            else:
                self.increaseExistingStat()
        return cost

    def sliceUp(self):
        cost=Mod.modSlicingCost[self.grade]
        self.grade=Mod.grades[Mod.grades.index(self.grade)+1]
        self.increaseExistingStat()
        return cost
        
    def getLevel(self):
        return self.level

    def getGrade(self):
        return self.grade

    def getGrades():
        return Mod.grades
    
    def getShape(self):
        return self.shape

    def getShapes():
        return Mod.shapes

    def getPips(self):
        return self.pips

    def getPrimary(self):
        return self.primary

    def getPrimaries():
        return Mod.primaries

    def getSecondary(self):
        return self.secondary

    def getSecondaries():
        return Mod.secondaries

    def getSellValue(self):
        return Mod.modSellingPrice[self.pips][self.level]

    def getSecondaryStatCount(self):
        return len(self.secondary.keys())

    def getSecondaryStatIncreaseCount(self):
        increases=0
        for stat in self.secondary:
            if stat=="speed":
                statIncreases=self.secondary[stat][0]
            else:
                statIncreases=self.secondary[stat]
            increases+=statIncreases-1
        return increases

    grades=["e","d","c","b","a"]
    grades6Dot=["6e", "6d", "6c", "6b", "6a"]
    allGrades=grades+grades6Dot

    gradeProbability={"a":2.3,"b":4.1,"c":10.3,"d":19.2,"e":64.1}
    
    shapes=["arrow","square","diamond","circle","cross","triangle"]
    shapeProbability={"arrow":10.3, "square":21.8, "diamond":24.4, "circle":23.9, "cross":13.1, "triangle":6.5}

    modSets=["crit chance", "crit dmg", "offense %", "defense %", "speed", "health %", "potency", "tenacity"]

    #qualities=["3 or 4 dots","5 dots","6 dots"]
    #qualitiesProbability={"3 or 4 dots":20,"5 dots":80,"6 dots":0}

    pipsProbability={1:0, 2:0, 3:10, 4:10, 5:80, 6:0}

    primariesProbability={ 
        "square":{"offense %":1},
        "diamond":{"defense %":1},
        "circle":{"health %":1,"protection %":1},
        "arrow":{"speed":1,"protection %":1,"health %":1,"crit avoidance":1,"defense %":1,"offense %":1,"accuracy":1},
        "triangle":{"crit dmg":1,"health %":1,"protection %":1,"offense %":1,"defense %":1, "crit chance":1},
        "cross":{"health %":1,"protection %":1,"offense %":1,"defense %":1,"potency":1,"tenacity":1}
    }

    primaries={}
    for shape in primariesProbability:
        primaries[shape]=[]
        for stat in primariesProbability[shape]:
            primaries[shape].append(stat)
    
    secondariesProbability={"offense":1,"offense %":1,"defense":1,"defense %":1,"health":1,"health %":1,
                            "protection":1,"protection %":1,"potency":1,"tenacity":1,"crit chance":1,"speed":1}
    
    secondaries=[]
    for stat in secondariesProbability:
        secondaries.append(stat)

    initialSpeedProbability={1:0, 2:0, 3:30.4, 4:34.1, 5:35.5}
    increaseSpeedProbability={1:0, 2:0, 3:18.9, 4:35.1, 5:37.9, 6:8.1}

    speedBumpsStr=["0", "1", "2", "3", "4", "5"]
    speedBumpsInt=range(0,6)

    modLevelingCost={
        5:{
            1:3450, 2:3450, 3:3450, 4:3450, 5:4600, 6:5750, 7:5750, 8:8050, 9:10300, 10:10300, 11:27650, 12:35650, 13:35650, 14:90850
        }
    }

    modSellingPrice={
        3:{
            1:3800
        },
        4:{
            1:6000
        },
        5:{
            1: 9500, 2:9500, 3:9500, 4:9500, 5:9500, 6:9500, 7:9500, 8:11700, 9:14900, 10:18900, 11:23000, 12:33800, 13:47700, 14:61700, 15:97200
        }
    }

    #material and credits
    modSlicingCost={    
            "e":{"mats":10,"credits":18000},
            "d":{"mats":20,"credits":36000},
            "c":{"mats":35,"credits":63000},
            "b":{"mats":50,"credits":90000},
            "a":{"capacitor":50, "amplifier":50, "modulator":20, "credits":200000},

            "6e":{"module":10, "credits":36000},
            "6d":{"module":10, "amplifier":5, "capacitor":5, "unit":10, "credits":72000},
            "6c":{"module":10, "amplifier":10, "capacitor":10, "unit":20, "resistor":10, "credits":126000 },
            "6b":{"capacitor":30, "modulator":10, "unit":20, "resistor":20, "microprocessor":15, "credits":276000 },
            "6a":{}
    }

    

    def getRndFromDistribution(probabilities):
        probabilitySpace=0
        for key in probabilities:
            probabilitySpace+=probabilities[key]

        randomInSpace=random.random()*probabilitySpace
        currentBoundary=0
        theRandom=0
        for key in probabilities:
            if randomInSpace<currentBoundary+probabilities[key]:
                theRandom=key
                break
            else:
                currentBoundary+=probabilities[key]
        #print(probabilities,randomInSpace, probabilitySpace, theRandom)
        assert(theRandom!=0)
        return(theRandom)
