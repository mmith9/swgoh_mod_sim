from datetime import datetime
from modsimulation import ModSimulation
from modAnalysis import *
from copy import deepcopy
from simSettings import *

import psutil
import math
import multiprocessing

class ModSimulationIteration:

    def __init__(self):
       
        ModSimulationIteration.manager=multiprocessing.Manager()
    
        self.enableMultiprocessing=False

        self.testlevel=20

        self.simSettings=SimSettings()
        self.simSettings.set("minSpeedToKeep", 10)
        
    def runSimsV1(self,countBranchOnly=False, benchmark=0):
        
        self.outputList=[]
        
        self.branchCount=0
        self.countBranchOnly=countBranchOnly
        self.benchmark=benchmark

        startTime = datetime.now()
        self.startUsedMem=psutil.virtual_memory()[3]

        returnDict="undefined"

        if self.enableMultiprocessing:
              
            self.processList=[]
     
            
            returnDict=ModSimulationIteration.manager.dict()

            self.pool=multiprocessing.Pool(4)

        self.walkGreyMaxInitialStats(returnDict)

        if self.enableMultiprocessing:
            #for process in self.processList:
            #    process.join()

            self.pool.close()
            self.pool.join()

            for branch in returnDict:
                self.outputList.append(returnDict[branch])
        
        endTime = datetime.now()
        print('Duration: {}'.format(endTime - startTime))
        if self.benchmark>0:
            print('Predicted full run: {}'.format((endTime - startTime)*100/benchmark))

        return self.outputList

    def walkGreyMaxInitialStats(self, returnDict):
        #complexity *5
        for maxStats in [0,1,2,3,4]:
            self.simSettings.set("uncoverStatsLimit", maxStats, grade="e")
            if self.testlevel>9:
                print("e stats", maxStats, end="| ")
            self.walkMinInitialSpeed(returnDict)

    def walkMinInitialSpeed(self, returnDict):
        #complexity 3^5
        #too severe and probably not worth on green+
        #simplyfying to only grey min initial speed
        #complexity *4

        #uncover 0 on grey means sell instantly
        if self.simSettings.uncoverStatsLimit["e"]["square"]==0:
            if self.testlevel>10:
                print("e min speed", 6, end="| ")       
            self.simSettings.set("minInitialSpeed", 6, grade="e")
            self.walkMinSpeedToSlice(returnDict)
        else:
            for minSpeed in [3,4,5]:
                self.simSettings.set("minInitialSpeed", minSpeed, grade="e")
                if self.testlevel>10:
                    print("e min speed", minSpeed, end="| ")               
                self.walkMinSpeedToSlice(returnDict)

    def walkMinSpeedToSlice(self, returnDict):
        #complexity 
        #
        #grey *1 as it's handled as min initial speed
        #green *9    speed range [3,4,5,6,7,8,9,10,11]
        #blue *11      speed range [3,4,| 5,6,7,8,10,11,12,13,14,15,| 16,17]
        #purple *13    speed range [3,4,5,6,| 7,8,10,11,12,13,14,15,16,17,18,19,| 20,21,22,23]
        #gold *1 no slicing necessary
        # plus grey<green<blue<purple constraint

        greenLowLimit=self.simSettings.minInitialSpeed["e"]["square"]
        if greenLowLimit==6:
            greenLowLimit=0

        greenLowLimit=max(greenLowLimit, 3) #green possible speed 3 to 2*6-1
        greenHighLimit=2*6-1
        for green in range(greenLowLimit,greenHighLimit): #blue in 3 to 3*6-1
            blueLowLimit=max(green, 3)
            blueHighLimit=3*6-2
            for blue in range(blueLowLimit,blueHighLimit): #purple in 3 to 4*6-1
                purpleLowLimit=max(blue, 3)
                purpleHighLimit=4*6-3
                for purple in range(purpleLowLimit,purpleHighLimit):

                    if self.testlevel>11:
                        print("d c b", green, blue, purple, end="| ")

                    self.simSettings.set("minSpeedToSlice", green,  grade="d" )
                    self.simSettings.set("minSpeedToSlice", blue,   grade="c" )
                    self.simSettings.set("minSpeedToSlice", purple, grade="b" )

                    self.walkRunSimWithSettingsStep1(returnDict)

    def walkRunSimWithSettingsStep1(self, returnDict):
        
        self.branchCount+=1

        if self.testlevel>7 :
            endUsedMem=psutil.virtual_memory()[3]
            memUsed=self.startUsedMem-endUsedMem
            print("sim number", self.branchCount, "mem used",math.trunc(memUsed/1024),"Kb",memUsed % 1024)

        if self.countBranchOnly:
            pass
        else:
            if (self.benchmark>0):
                if (self.branchCount % (100/self.benchmark))==0:
                    self.walkRunSimWithSettingsStep2(returnDict)                    
            else:
                self.walkRunSimWithSettingsStep2(returnDict)

    def walkRunSimWithSettingsStep2(self, returnDict):
        currentSettings=deepcopy(self.simSettings.getAll())

        if not self.enableMultiprocessing:            
            outcome=ModSimulationIteration.walkRunSimWithSettings(currentSettings)
            self.outputList.append(outcome)
        else:       
            if self.testlevel>8:
                print("ProcSpawn ",end="")
            branchCount=self.branchCount

            self.pool.apply_async(ModSimulationIteration.walkRunSimWithSettingsWrapper, (currentSettings, branchCount, returnDict))
            
    def walkRunSimWithSettingsWrapper(currentSettings, currentBranch, returnDict):
        print(psutil.virtual_memory())
        
        output=ModSimulationIteration.walkRunSimWithSettings(currentSettings)
        returnDict[currentBranch] = output
       
        print("process done")

    def walkRunSimWithSettings(currentSettings):

        modSim=ModSimulation()
        analysis = modSim.walkIt(currentSettings)

        analysis.calcScores(analysis.energyFactor)
        scores=analysis.getScores()
        costs=analysis.budget.getAll()
        
        
        return {"scores":scores, "settings":currentSettings, "costs":costs}

def rtValueHigh(x):
    return x["scores"]["speedValue"]["high"]

def rtValueMid(x):
    return x["scores"]["speedValue"]["mid"]
    
def rtValueLow(x):
    return x["scores"]["speedValue"]["low"]
    
def rtValueElisa(x):
    return x["scores"]["speedValue"]["Elisa"]
        
def rtValueElisaM14(x):
    return x["scores"]["speedValue"]["ElisaM14"]
    







