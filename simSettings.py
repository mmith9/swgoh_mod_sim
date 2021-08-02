from mod import Mod
from copy import deepcopy
import math
import json

class SimSettings:

    def __init__(self):
        self.testlevel=1

        self.generatedSettings=0
        self.iterationCount=0
        self.fileCount=0
                
        self.general={
            "sellAccuracyArrows":1, "keepSpeedArrows":1, "ignoreRestOfArrows":1
            ,"sellNoSpeedMods":1, "sellTooLowInitialSpeedMods":1, "sellTooSlowFinalMods":1
            ,"allowSpeedBumpMisses":1
            ,"enable6DotSlicing":1
            ,"convertMats1-4ToEnergy":1
            ,"creditsLimit":"half", "shipCreditsLimit":"half"
            ,"modSet":"offense"
            ,"quickPrimaryForking":1, "quickSecondaryForking":1, "quickSpeedForking":1
            ,"quickSDCForking":1, "quickSDCandCForking":1, "quickSDCCTForking":1
            }

        self.modStore={
            "enableShopping":True,
            "spendCredits":True,
            "spendShipCredits":True,

            "wishList":[
                {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
            ]
        }       
        
            
        # level up mod to uncover stats DEFAULT 4 = uncover all
        self.uncoverStatsLimit={} #2 dimension dict  GRADE x SHAPE
        for grade in Mod.grades:
            self.uncoverStatsLimit[grade]={}
            for shape in Mod.shapes:
                self.uncoverStatsLimit[grade][shape]=4

        # If mod got speed uncovered, this is the limit when to sell DEFAULT 0
        self.minInitialSpeed={} #2 dimension dict, GRADE x SHAPE
        for grade in Mod.grades:
            self.minInitialSpeed[grade]={}
            for shape in Mod.shapes:
                self.minInitialSpeed[grade][shape]=0

        self.minSpeedToSlice={} #3 dimension dict. DEFAULT 0   BUMPS x ALL GRADE x SHAPE
        for speedBumps in range(0,6):
            self.minSpeedToSlice[speedBumps]={}
            for grade in Mod.allGrades:
                self.minSpeedToSlice[speedBumps][grade]={}
                for shape in Mod.shapes:
                    self.minSpeedToSlice[speedBumps][grade][shape]=0

        self.minSpeedToKeep={} #3 dimension dict. DEFAULT 0 speed BUMPS x ALL GRADE x SHAPE
        for speedBumps in range(0,6):
            self.minSpeedToKeep[speedBumps]={}
            for grade in Mod.allGrades:
                self.minSpeedToKeep[speedBumps][grade]={}
                for shape in Mod.shapes:
                    self.minSpeedToKeep[speedBumps][grade][shape]=0

    def getAll(self):
        # NECCESARY FOR MULTIPROCESSING
        # modsimulation takes argument in this form, objects are bad, dictionaries are ok
        settings={

            "general" : self.general
            ,"minInitialSpeed": self.minInitialSpeed
            ,"uncoverStatsLimit": self.uncoverStatsLimit
            ,"minSpeedToSlice": self.minSpeedToSlice
            ,"minSpeedToKeep": self.minSpeedToKeep
            ,"modStore": self.modStore
        }
        return settings

    def set(self, target, value, grade="any", shape="any", speedBumps="any"):      
        # example:  settings.set("minSpeedToSlice", grade=any, shape=any,)
        if grade=="any":
            if target in ["minSpeedToKeep", "minSpeedToSlice"]:
                for gradeExpand in Mod.allGrades:
                    self.setIterateShape(target, gradeExpand, shape, speedBumps, value)    
                
            else:
                for gradeExpand in Mod.grades:
                    self.setIterateShape(target, gradeExpand, shape, speedBumps, value)    

        elif type(grade) is list:
            for gradeExpand in grade:
                self.setIterateShape(target, gradeExpand, shape, speedBumps, value)
        else:
            self.setIterateShape(target, grade, shape, speedBumps, value)

    def setIterateShape(self, target, grade, shape, speedBumps, value ):
        if shape=="any":
            for shapeExpand in Mod.shapes:
                self.setIterateSpeedBumps(target, grade, shapeExpand, speedBumps, value)
        elif type(shape) is list:
            for shapeExpand in shape:
                self.setIterateSpeedBumps(target, grade, shapeExpand, speedBumps, value)
        else:
            self.setIterateSpeedBumps(target, grade, shape, speedBumps, value)

    def setIterateSpeedBumps(self, target, grade, shape, speedBumps, value):
        if speedBumps=="any":
            for speedBumpsExpand in range (0,6):
                self.setIterateTheSet(target, grade, shape, speedBumpsExpand, value)
        elif type(speedBumps) is list:
            for speedBumpsExpand in speedBumps:
                self.setIterateTheSet(target, grade, shape, speedBumpsExpand, value)
        else:
            self.setIterateTheSet(target, grade, shape, speedBumps, value)

    def setIterateTheSet(self, target, grade, shape, speedBumps, value):
        if target=="uncoverStatsLimit":
            self.uncoverStatsLimit[grade][shape]=value

        if target=="minInitialSpeed":
            self.minInitialSpeed[grade][shape]=value
        
        if target=="minSpeedToSlice":
            self.minSpeedToSlice[speedBumps][grade][shape]=value
        
        if target=="minSpeedToKeep":
            self.minSpeedToKeep[speedBumps][grade][shape]=value

    def iterateSettingsByList(self, iterateList, listPosition=0, iteratedList=[], countBranchOnly=0, benchmarkPercent=0, outputPrefix="none", fileCut=0, sanityConstraint=0):
        if listPosition==0:
            self.generatedSettings=0

        #iterate further down the list?
        if listPosition < len(iterateList):
            currentIteration=iterateList[listPosition]
           
            for x in currentIteration["range"]:
                self.set(currentIteration["target"], x, grade=currentIteration["grade"], shape=currentIteration["shape"], speedBumps=currentIteration["speedBumps"])
                self.iterateSettingsByList(iterateList, listPosition+1, iteratedList, countBranchOnly, benchmarkPercent, outputPrefix, fileCut, sanityConstraint)

        #nope all on list has been iterated 
        else:
            self.iterationCount+=1
            if (self.testlevel>0) and (self.iterationCount % 10000 == 0):
                print(".", end="")
               
            if (sanityConstraint==1) and not self.iterateCheckSanity() :
                pass

            elif countBranchOnly>0 :
                self.generatedSettings+=1
                if (self.testlevel>0) and (self.generatedSettings % 10000 == 0):
                    print("*", end="")
                pass

            else:
                self.generatedSettings+=1
                if (self.testlevel>0) and (self.generatedSettings % 1000 == 0):
                    print("*", end="")
                    
                if benchmarkPercent>0:
                    if (self.generatedSettings % (benchmarkPercent*100) == 0):
                        self.iterateStep2(iteratedList, outputPrefix, fileCut)
                else:
                    self.iterateStep2(iteratedList, outputPrefix, fileCut)

                #print(self.generatedSettings)
                #print(self.generatedSettings, fileCut)
                if outputPrefix!="none" and fileCut>0:
                    #print(self.generatedSettings, fileCut)
                    if (self.generatedSettings % fileCut) == 0:
                        print("save")
                        self.iterateSaveToFiles(iteratedList, outputPrefix, fileCut)
            
        #means original function call, and iterations done
        if listPosition==0: 
            if countBranchOnly>0:
                return self.generatedSettings
            elif outputPrefix!="none":
                self.iterateSaveToFiles(iteratedList, outputPrefix, fileCut)
                return outputPrefix
            else:
                return iteratedList

    def iterateStep2(self, iteratedList, outputPrefix, fileCut ):
        settingsCopy=deepcopy(self.getAll())
        iteratedList.append([self.generatedSettings, settingsCopy])

    def iterateSaveToFiles(self, iteratedList, outputPrefix, fileCut):
        if fileCut>0:
            cutFileName="iteration_results/"+outputPrefix+str(self.fileCount)+"x"+str(fileCut)+".json"
            self.fileCount+=1
        else:
           cutFileName="iteration_results/"+outputPrefix+".json"
    
        with open(cutFileName, "w") as fp:
            json.dump(iteratedList, fp)
        iteratedList.clear()

    def iterateCheckSanity(self):
        #print("sanity check")
        sanity=True
        shapesToCheck=["square"]

        # actually no sense, can set to 0 and let min inital speed for grey do the job
        #
        # first, minSpeedToSlice for grey >= minInitialSpeed for grey
        #for shape in Mod.shapes:
        #    sanity=sanity and (self.minSpeedToSlice[1]["e"][shape] >= self.minInitialSpeed["e"][shape])


        #checking if minSpeedToSlice for speedBumps and grade satisfies <= for speedBumps+1 or grade+1, but ignore if 0 as those are not iterated and relevant
        # 
        #

                    
        for speedBumps in range(0,5) :
            for grade in ["e", "d", "c", "b", "a"]:
                for shape in shapesToCheck:                        

                    tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
                    tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps+1][grade][shape])
                    sanity=sanity and tmpBool

                    if (self.testlevel == 4) and not tmpBool:
                        print(speedBumps, speedBumps+1, grade, shape, Mod.grades.index(grade))
                        print(self.minSpeedToSlice[speedBumps][grade][shape])
                        print(self.minSpeedToSlice[speedBumps+1][grade][shape])

        for speedBumps in range(0,6) :
            for grade in ["e", "d", "c", "b"]:
                nextGrade=Mod.grades[Mod.grades.index(grade)+1]
                for shape in shapesToCheck:                         

                    tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
                    tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
                    sanity=sanity and tmpBool

                    if (self.testlevel == 2) and not tmpBool:
                        print(speedBumps, grade, nextGrade, shape)
                        print(self.minSpeedToSlice[speedBumps][grade][shape])
                        print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

        #gap at 6 dot slice
        for speedBumps in range(0,6) :
            for shape in shapesToCheck:                        
                tmpBool=(self.minSpeedToSlice[speedBumps]["a"][shape] == 100)
                tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps]["a"][shape] < self.minSpeedToSlice[speedBumps]["6e"][shape])
                sanity=sanity and tmpBool

        for speedBumps in range(0,6) :
            for grade in ["6e", "6d", "6c", "6b"]:
                nextGrade=Mod.allGrades[Mod.allGrades.index(grade)+1]
                for shape in shapesToCheck:                         

                    tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
                    tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
                    sanity=sanity and tmpBool

                    if (self.testlevel == 2) and not tmpBool:
                        print(speedBumps, grade, nextGrade, shape)
                        print(self.minSpeedToSlice[speedBumps][grade][shape])
                        print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

        return sanity