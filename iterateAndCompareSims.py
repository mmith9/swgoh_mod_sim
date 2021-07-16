from datetime import datetime
from modsimulation import ModSimulation
from modAnalysis import *
from copy import deepcopy
from modStore import *
import psutil
import math

class ModSimulationIteration():
    
    def __init__(self):

        self.modStore=ModStore()
        self.simList=[]
        self.enableThreading=False

        self.testlevel=10

        resources={"dailyEnergy":645, "dailyCredits":900000}

        general={"sellAccuracyArrows":1, "keepSpeedArrows":1, "ignoreRestOfArrows":1,
            "sellNoSpeedMods":1, "sellTooLowInitialSpeedMods":1, "modSet":"offense",
            "quickPrimaryForking":1, "quickSecondaryForking":1, "quickSpeedForking":1,
            "greyMaxInitialStats":4
            }
            
        #initial speed = 3 4 5 | set 6 to sell given grade
        minInitialSpeed={
            "e":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "d":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "c":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "b":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "a":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}
        }

        #lev12 speed = 3/4/5 + 3/4/5/6 per grade
        minLev12Speed={
            "e":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "d":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "c":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "b":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "a":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}   
        }

        # 0 - do not allow misses
        minSpeedIfBumpMissed={
            "e":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "d":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0},
            "c":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "b":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}, 
            "a":{"square":0, "arrow":0, "diamond":0, "triangle":0, "circle":0, "cross":0}   
        }

        self.settings={"resources" : resources, "general" : general, "minInitialSpeed": minInitialSpeed, "minLev12Speed":minLev12Speed, "minSpeedIfBumpMissed":minSpeedIfBumpMissed}

    def runSimsV1(self,countBranchOnly=False, benchmark=0):
        
        self.simList=[]
        
        self.branchCount=0
        self.countBranchOnly=countBranchOnly
        self.benchmark=benchmark

        startTime = datetime.now()
        self.walkGreyMaxInitialStats()
        endTime = datetime.now()
        print('Duration: {}'.format(endTime - startTime))

    def walkGreyMaxInitialStats(self):
        #complexity *5
        for maxStats in [0,1,2,3,4]:
            self.settings["general"]["greyMaxInitialStats"]=maxStats
            self.walkMinInitialSpeed()
    
    def walkMinInitialSpeed(self):
        #complexity 3^5
        #too severe and probably not worth on green+
        #simplyfying to only grey min initial speed
        #complexity *4

        if self.settings["general"]["greyMaxInitialStats"]==0:
            #can't uncover stats, means sell right away
            for shape in Mod.shapes:
                self.settings["minInitialSpeed"]["e"][shape]=6
            self.walkMinSpeedToSlice()
        else:
            for minSpeed in [3,4,5]:
                for shape in Mod.shapes:
                    self.settings["minInitialSpeed"]["e"][shape]=minSpeed
                self.walkMinSpeedToSlice()
        
    def walkMinSpeedToSlice(self):
        #complexity 
        #
        #grey *1 as it's handled as min initial speed
        #green *9    speed range [3,4,5,6,7,8,9,10,11]
        #blue *11      speed range [3,4,| 5,6,7,8,10,11,12,13,14,15,| 16,17]
        #purple *13    speed range [3,4,5,6,| 7,8,10,11,12,13,14,15,16,17,18,19,| 20,21,22,23]
        #gold *1 no slicing necessary
        # plus grey<green<blue<purple constraint

        if self.settings["minInitialSpeed"]["e"]["square"]==6:
            greenLowLimit=3
        else:
            greenLowLimit=self.settings["minInitialSpeed"]["e"]["square"]
        
        greenLowLimit=max(greenLowLimit, 3) #green possible speed 3 to 2*6-1
        greenHighLimit=2*6-1
        for green in range(greenLowLimit,greenHighLimit): #blue in 3 to 3*6-1
            blueLowLimit=max(green, 3)
            blueHighLimit=3*6-2
            for blue in range(blueLowLimit,blueHighLimit): #purple in 3 to 4*6-1
                purpleLowLimit=max(blue, 3)
                purpleHighLimit=4*6-3
                for purple in range(purpleLowLimit,purpleHighLimit):
                    for shape in Mod.shapes:
                        self.settings["minLev12Speed"]["d"][shape]=green
                        self.settings["minSpeedIfBumpMissed"]["d"][shape]=green

                        self.settings["minLev12Speed"]["c"][shape]=blue
                        self.settings["minSpeedIfBumpMissed"]["c"][shape]=blue
                        
                        self.settings["minLev12Speed"]["b"][shape]=purple
                        self.settings["minSpeedIfBumpMissed"]["b"][shape]=purple
                        
                    self.walkRunSimWithSettingsStep1()

    def walkRunSimWithSettingsStep1(self):
        
        self.branchCount+=1
        if self.countBranchOnly:
            pass
        else:
            if (self.benchmark>0):
                if (self.branchCount % (100/self.benchmark))==0:
                    self.walkRunSimWithSettingsStep2()                    
            else:
                self.walkRunSimWithSettingsStep2()

    def walkRunSimWithSettingsStep2(self):

        if self.enableThreading==True:
            pass

        else:
            outcome=self.walkRunSimWithSettings()
            self.simList.append(outcome)
            pass

    def walkRunSimWithSettings(self):
        startUsedMem=psutil.virtual_memory()[3]

        currentSettings=deepcopy(self.settings)
        modSim=ModSimulation()
        analysis = modSim.walkIt(currentSettings)

        energyCost=-analysis.avgEnergyChange
        creditCost=-analysis.avgCreditsChange

        dailyFactor=currentSettings["resources"]["dailyEnergy"]/energyCost
        budget=currentSettings["resources"]["dailyCredits"]-creditCost*dailyFactor
        if self.testlevel>10:
            print("budget for mods",budget)

        wishlist=[
                {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
            ]
        boughtItems=self.modStore.modShopping(budget, wishlist)
        item=boughtItems[0]
        modSim.walkBoughtMod(item["dailyProbability"]/dailyFactor, item["mod"])
        modSim.creditChange(1 / dailyFactor, -item["dailyCreditCost"])

        analysis.calcScores(dailyFactor)

        endUsedMem=psutil.virtual_memory()[3]
        memUsed=startUsedMem-endUsedMem
        if self.testlevel>1:
            print("sim number", self.branchCount, "mem used",math.trunc(memUsed/1024),"Kb",memUsed % 1024)
            print(analysis.speedValue)
            print(psutil.virtual_memory())
       
        return {"analysis":analysis, "settings":currentSettings}

def rtValueHigh(sim):
    return sim["analysis"].speedValue["high"]
def rtValueMid(sim):
    return sim["analysis"].speedValue["mid"]
def rtValueLow(sim):
    return sim["analysis"].speedValue["low"]
def rtValueElisa(sim):
    return sim["analysis"].speedValue["Elisa"]
def rtValueElisaM14(sim):
    return sim["analysis"].speedValue["ElisaM14"]







