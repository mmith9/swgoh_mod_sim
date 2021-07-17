from datetime import datetime
from modsimulation import ModSimulation
from modAnalysis import *
from copy import deepcopy

import psutil
import math
import multiprocessing

class ModSimulationIteration():

    def __init__(self):
       
        ModSimulationIteration.manager=multiprocessing.Manager()
    
        self.enableMultiprocessing=True

        self.testlevel=10

        resources={"dailyEnergy":645, "dailyCredits":900000}

        general={"sellAccuracyArrows":1, "keepSpeedArrows":1, "ignoreRestOfArrows":1,
            "sellNoSpeedMods":1, "sellTooLowInitialSpeedMods":1, "sellTooSlowFinalMods":1,
            "modSet":"offense",
            "quickPrimaryForking":1, "quickSecondaryForking":1, "quickSpeedForking":1,
            "greyMaxInitialStats":4
            }

        modStore={"enableShopping":True,
            "wishList":[
                {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
            ]
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

        self.settings={"resources" : resources, "general" : general, "minInitialSpeed": minInitialSpeed, "minLev12Speed":minLev12Speed, "minSpeedIfBumpMissed":minSpeedIfBumpMissed, "modStore":modStore}

    def runSimsV1(self,countBranchOnly=False, benchmark=0):
        
        self.outputList=[]
        
        self.branchCount=0
        self.countBranchOnly=countBranchOnly
        self.benchmark=benchmark

        startTime = datetime.now()

        returnDict="undefined"

        if self.enableMultiprocessing:
              
            self.processList=[]
            self.mpOutputList=[]
            
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
            self.settings["general"]["greyMaxInitialStats"]=maxStats
            self.walkMinInitialSpeed(returnDict)
    
    def walkMinInitialSpeed(self, returnDict):
        #complexity 3^5
        #too severe and probably not worth on green+
        #simplyfying to only grey min initial speed
        #complexity *4

        if self.settings["general"]["greyMaxInitialStats"]==0:
            #can't uncover stats, means sell right away
            for shape in Mod.shapes:
                self.settings["minInitialSpeed"]["e"][shape]=6
            self.walkMinSpeedToSlice(returnDict)
        else:
            for minSpeed in [3,4,5]:
                for shape in Mod.shapes:
                    self.settings["minInitialSpeed"]["e"][shape]=minSpeed
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
                        
                    self.walkRunSimWithSettingsStep1(returnDict)

    def walkRunSimWithSettingsStep1(self, returnDict):
        
        self.branchCount+=1
        if self.countBranchOnly:
            pass
        else:
            if (self.benchmark>0):
                if (self.branchCount % (100/self.benchmark))==0:
                    self.walkRunSimWithSettingsStep2(returnDict)                    
            else:
                self.walkRunSimWithSettingsStep2(returnDict)

    def walkRunSimWithSettingsStep2(self, returnDict):

        if not self.enableMultiprocessing:
            currentSettings=deepcopy(self.settings)
            outcome=self.walkRunSimWithSettings(currentSettings)
            self.outputList.append(outcome)
        else:
            currentSettings=deepcopy(self.settings)
            #wait permission to spawn
            print("spawn")

            branchCount=self.branchCount

            self.pool.apply_async(ModSimulationIteration.walkRunSimWithSettingsWrapper, (currentSettings, branchCount, returnDict))
            # workerProcess=multiprocessing.Process(target=ModSimulationIteration.walkRunSimWithSettingsWrapper, args=(currentSettings, branchCount, returnDict))
            # self.processList.append(workerProcess)
            # workerProcess.start()
            
    def walkRunSimWithSettingsWrapper(currentSettings, currentBranch, returnDict):
        print(psutil.virtual_memory())
        startUsedMem=psutil.virtual_memory()[3]

        output=ModSimulationIteration.walkRunSimWithSettings(currentSettings)
        returnDict[currentBranch] = output
        endUsedMem=psutil.virtual_memory()[3]
        memUsed=startUsedMem-endUsedMem
        print("sim number", currentBranch, "mem used",math.trunc(memUsed/1024),"Kb",memUsed % 1024)
        
        #ModSimulationIteration.processSemaphore.release()

        print("process done")

    def walkRunSimWithSettings(currentSettings):

        modSim=ModSimulation()
        analysis = modSim.walkIt(currentSettings)

        dailyFactor=analysis.costs["dailyFactor"]

        analysis.calcScores(dailyFactor)
        scores=analysis.getScores()
        costs=analysis.costs
        #print(scores)#
        
        return {"scores":scores, "settings":currentSettings, "cost":costs}

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
    







