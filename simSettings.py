from json.encoder import py_encode_basestring_ascii
from mod import Mod
from copy import deepcopy
import json
import binascii

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

                if self.testlevel>2:
                    print(self.settingsFingerprint()," ", end="")
                    print(self.settingsHash())
                    print("fingerprint:",len(self.settingsFingerprint()), "settings:", len(json.dumps(self.getAll())))

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
        iteratedList.append([self.generatedSettings, settingsCopy, self.settingsFingerprint(), self.settingsHash()])

    def iterateSaveToFiles(self, iteratedList, outputPrefix, fileCut):
        if fileCut>0:
            cutFileName="iteration_results/"+outputPrefix +"x" +str(self.fileCount)+".json"
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
            for grade in Mod.allGrades:
                for shape in shapesToCheck:                        

                    tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
                    tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps+1][grade][shape])
                    sanity=sanity and tmpBool

                    if (self.testlevel == 4) and not tmpBool:
                        print(speedBumps, speedBumps+1, grade, shape, Mod.grades.index(grade))
                        print(self.minSpeedToSlice[speedBumps][grade][shape])
                        print(self.minSpeedToSlice[speedBumps+1][grade][shape])

        for speedBumps in range(0,6) :
            for grade in ["e", "d", "c", "b", "a", "6e", "6d", "6c", "6b"]:
                if grade=="a":
                    speedAdjust=1
                else:
                    speedAdjust=0

                nextGrade=Mod.allGrades[Mod.allGrades.index(grade)+1]
                for shape in shapesToCheck:                         

                    tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
                    tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] + speedAdjust <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
                    sanity=sanity and tmpBool

                    if (self.testlevel == 2) and not tmpBool:
                        print(speedBumps, grade, nextGrade, shape)
                        print(self.minSpeedToSlice[speedBumps][grade][shape])
                        print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

        # #gap at 6 dot slice
        # for speedBumps in range(0,6) :
        #     for shape in shapesToCheck:                        
        #         tmpBool=(self.minSpeedToSlice[speedBumps]["a"][shape] == 100)
        #         tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps]["a"][shape] < self.minSpeedToSlice[speedBumps]["6e"][shape])
        #         sanity=sanity and tmpBool

        # for speedBumps in range(0,6) :
        #     for grade in ["6e", "6d", "6c", "6b"]:
        #         nextGrade=Mod.allGrades[Mod.allGrades.index(grade)+1]
        #         for shape in shapesToCheck:                         

        #             tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
        #             tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
        #             sanity=sanity and tmpBool

        #             if (self.testlevel == 2) and not tmpBool:
        #                 print(speedBumps, grade, nextGrade, shape)
        #                 print(self.minSpeedToSlice[speedBumps][grade][shape])
        #                 print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

        return sanity

    def settingsFingerprint(self) -> str:
        return SimSettings.settingsFingerprintOfGetAll(self.getAll())
        
    def settingsFingerprintOfGetAll(settings) -> str:
        fingerprint=""
        
        ### HOTFIX
        bump1=1
        bump2=2
        bump3=3
        bumpRange=range(1,5)

        for x in settings["minSpeedToSlice"].keys():
            if type(x) == str:
                bump1="1"
                bump2="2"
                bump3="3"
                bumpRange=["1", "2", "3", "4"]
            break                 

        fingerprint+=str(settings["uncoverStatsLimit"]["e"]["square"])
        fingerprint+=str(settings["uncoverStatsLimit"]["d"]["square"])
        
        fingerprint+=str(settings["minInitialSpeed"]["e"]["square"])
        fingerprint+=str(settings["minInitialSpeed"]["d"]["square"])

        fingerprint+=str(settings["minSpeedToSlice"][bump1]["e"]["square"])

        fingerprint+=str(settings["minSpeedToSlice"][bump1]["d"]["square"])
        fingerprint+=str(settings["minSpeedToSlice"][bump2]["d"]["square"])

        fingerprint+=str(settings["minSpeedToSlice"][bump1]["c"]["square"])
        fingerprint+=str(settings["minSpeedToSlice"][bump2]["c"]["square"])
        fingerprint+=str(settings["minSpeedToSlice"][bump3]["c"]["square"])
        
        

        for grade in ["a", "6e", "6d", "6c", "6b"]:
            for speedBumps in bumpRange:
                fingerprint+=str(settings["minSpeedToSlice"][speedBumps][grade]["square"])
        
        return fingerprint

    def settingsHash(self) -> int:
        ### HOTFIX
        return SimSettings.settingsHashOfGetAll(json.loads(json.dumps(self.getAll())))
    
    def settingsHashOfGetAll(settings) -> int:
        return binascii.crc32(bytes(json.dumps(settings), "utf-8"))
    
    def iterateSettingsByListQuick(self, iterateList, listPosition=0, iteratedList=[], complexityList=[], countBranchOnly=0, benchmarkPercent=0, outputPrefix="none", fileCut=0, sanityConstraint=1):
        if not complexityList:
            self.calculateComplexity(iterateList, complexityList)
            self.iterationBranchesTotal=complexityList[0]
            self.iteratedBranches=0
            self.generatedSettings=0
            assert(listPosition==0)

        if self.testlevel>10:
            print("level:",listPosition, "complexity:",complexityList[listPosition], "branches:", self.iteratedBranches, "of", self.iterationBranchesTotal, 
                "(", self.iteratedBranches/self.iterationBranchesTotal*100,"% )")

            if listPosition<len(iterateList):
                print(iterateList[listPosition])
            
            if self.testlevel>20:
                input()
 
        #iterate further down the list?
        if listPosition < len(iterateList):
            currentIteration=iterateList[listPosition]
           
            for x in currentIteration["range"]:
                self.set(currentIteration["target"], x, grade=currentIteration["grade"], shape=currentIteration["shape"], speedBumps=currentIteration["speedBumps"])
                if self.iterateCheckSanityPartialQuick(iterateList, listPosition):
                    self.iterateSettingsByListQuick(iterateList, listPosition+1, iteratedList, complexityList, countBranchOnly, benchmarkPercent, outputPrefix, fileCut, sanityConstraint)
                else:
                    if self.testlevel>9:
                        print("partial sanity branch cut, list pos:", listPosition, "branches cut:", complexityList[listPosition+1])
                    self.iteratedBranches+= complexityList[listPosition+1]

        #nope all on list has been iterated 
        else:
            self.iterationCount+= 1
            self.iteratedBranches+= 1

            if (self.testlevel>0) and (self.iterationCount % 10000 == 0):
                #print(".", end="")
                pass

            if (self.testlevel>0) and (self.iterationCount % 100 == 0):
                print("branches:", self.iteratedBranches, "of", self.iterationBranchesTotal, 
                "(", self.iteratedBranches/self.iterationBranchesTotal*100,"% )", "valid settings produced", self.generatedSettings )
              
            # Because allready checked by partial sanity, last step is not partial but full   
            #assert(self.iterateCheckSanity() == True)
            
            if (sanityConstraint==1) and not self.iterateCheckSanity() :
                pass

            elif countBranchOnly>0 :
                self.generatedSettings+=1

                if self.testlevel>20:
                    print(self.settingsFingerprint()," ", end="")
                    print(self.settingsHash())
                    print("fingerprint:",len(self.settingsFingerprint()), "settings:", len(json.dumps(self.getAll())))

                if (self.testlevel>0) and (self.generatedSettings % 10000 == 0):
                    #print("*", end="")
                    pass

            else:
                self.generatedSettings+=1
                if (self.testlevel>0) and (self.generatedSettings % 1000 == 0):
                    #print("*", end="")
                    pass
                    
                if benchmarkPercent>0:
                    if (self.generatedSettings % (benchmarkPercent*100) == 0):
                        self.iterateStep2(iteratedList, outputPrefix, fileCut)
                else:
                    self.iterateStep2(iteratedList, outputPrefix, fileCut)


                if outputPrefix!="none" and fileCut>0:
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

    def calculateComplexity(self, iterateList, complexityList):
        for baseLevel in range(0, len(iterateList)):
            complexity=1
            for level in range(baseLevel, len(iterateList)):
                complexity*= len(iterateList[level]["range"])
            complexityList.append(complexity)
        complexityList.append(1)

    def iterateCheckSanityPartial(self, iterateList, listPosition)-> bool:
        assert(False)

    #     #print("sanity check")
    #     sanity=True
    #     shapesToCheck=["square"]

    #     # actually no sense, can set to 0 and let min inital speed for grey do the job
    #     #
    #     # first, minSpeedToSlice for grey >= minInitialSpeed for grey
    #     #for shape in Mod.shapes:
    #     #    sanity=sanity and (self.minSpeedToSlice[1]["e"][shape] >= self.minInitialSpeed["e"][shape])


    #     #checking if minSpeedToSlice for speedBumps and grade satisfies <= for speedBumps+1 or grade+1, but ignore if 0 as those are not iterated and relevant
    #     # 
    #     #

    #     ## first check increase in speedbumps            
    #     for speedBumps in range(0,5) :
    #         for grade in Mod.allGrades:
    #             for shape in shapesToCheck:                        
                    
    #                 isFirstArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, grade, shape)
    #                 isSecondArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps+1, grade, shape)

    #                 if isFirstArgOnList and isSecondArgOnList:
    #                     tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
    #                     tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps+1][grade][shape])
    #                     sanity=sanity and tmpBool

    #                     if (self.testlevel == 4) and not tmpBool:
    #                         print(speedBumps, speedBumps+1, grade, shape, Mod.grades.index(grade))
    #                         print(self.minSpeedToSlice[speedBumps][grade][shape])
    #                         print(self.minSpeedToSlice[speedBumps+1][grade][shape])

    #     ## second check increase in grade from "e" to "a"
    #     for speedBumps in range(0,6) :
    #         for grade in ["e", "d", "c", "b"]:
    #             nextGrade=Mod.grades[Mod.grades.index(grade)+1]
    #             for shape in shapesToCheck:                         

    #                 isFirstArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, grade, shape)
    #                 isSecondArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, nextGrade, shape)
                    
    #                 if isFirstArgOnList and isSecondArgOnList:
    #                     tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
    #                     tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
    #                     sanity=sanity and tmpBool

    #                     if (self.testlevel == 2) and not tmpBool:
    #                         print(speedBumps, grade, nextGrade, shape)
    #                         print(self.minSpeedToSlice[speedBumps][grade][shape])
    #                         print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

    #     ## third check gap at "a" to "6e" slice , speed+1 !
    #     #gap at 6 dot slice
    #     for speedBumps in range(0,6) :
    #         for shape in shapesToCheck:                    
                
    #             isFirstArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, "a", shape)
    #             isSecondArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, "6e", shape)

    #             if isFirstArgOnList and isSecondArgOnList:
    #                 tmpBool=(self.minSpeedToSlice[speedBumps]["a"][shape] == 100)
    #                 tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps]["a"][shape] < self.minSpeedToSlice[speedBumps]["6e"][shape])
    #                 sanity=sanity and tmpBool

    #     ## 4th, check grade increase from "6e" to "6a"
    #     for speedBumps in range(0,6) :
    #         for grade in ["6e", "6d", "6c", "6b"]:
    #             nextGrade=Mod.allGrades[Mod.allGrades.index(grade)+1]
    #             for shape in shapesToCheck:                         

    #                 isFirstArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, grade, shape)
    #                 isSecondArgOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumps, nextGrade, shape)

    #                 if isFirstArgOnList and isSecondArgOnList:
    #                     tmpBool=(self.minSpeedToSlice[speedBumps][grade][shape] == 100)
    #                     tmpBool=tmpBool or (self.minSpeedToSlice[speedBumps][grade][shape] <= self.minSpeedToSlice[speedBumps][nextGrade][shape])
    #                     sanity=sanity and tmpBool

    #                     if (self.testlevel == 2) and not tmpBool:
    #                         print(speedBumps, grade, nextGrade, shape)
    #                         print(self.minSpeedToSlice[speedBumps][grade][shape])
    #                         print(self.minSpeedToSlice[speedBumps][nextGrade][shape])

    #     return sanity

    def iterateCheckSanityPartialQuick(self, iterateList, listPosition) -> bool :

        sanity=True
        shapesToCheck=["square"]

        currShape="square"  #shortcut
        currGrade=iterateList[listPosition]["grade"]
        currSpeedBumps=iterateList[listPosition]["speedBumps"]

        if currGrade!="e":
            gradeDown=Mod.allGrades[Mod.allGrades.index(currGrade)-1]
            isGradeDownOnList=self.isSettingOnPartialList(iterateList, listPosition, currSpeedBumps, gradeDown, currShape)
        else:
            isGradeDownOnList=False
        
        if currGrade!="6a":
            gradeUp=Mod.allGrades[Mod.allGrades.index(currGrade)+1]
            isGradeUpOnList=self.isSettingOnPartialList(iterateList, listPosition, currSpeedBumps, gradeUp, currShape)
        else:
            isGradeUpOnList=False

        if currSpeedBumps!=0:
            speedBumpsDown=currSpeedBumps-1
            isSpeedBumpsDownOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumpsDown, currGrade, currShape)
        else:
            isSpeedBumpsDownOnList=False

        if currSpeedBumps!=5:
            speedBumpsUp=currSpeedBumps+1
            isSpeedBumpsUpOnList=self.isSettingOnPartialList(iterateList, listPosition, speedBumpsUp, currGrade, currShape)
        else:
            isSpeedBumpsUpOnList=False


        if isSpeedBumpsDownOnList:
            tmpBool=(self.minSpeedToSlice[speedBumpsDown][currGrade][currShape] == 100)
            tmpBool=tmpBool or (self.minSpeedToSlice[speedBumpsDown][currGrade][currShape] <= self.minSpeedToSlice[currSpeedBumps][currGrade][currShape])
            sanity=sanity and tmpBool

        if isSpeedBumpsUpOnList:
            tmpBool=(self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] == 100)
            tmpBool=tmpBool or (self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] <= self.minSpeedToSlice[speedBumpsUp][currGrade][currShape])
            sanity=sanity and tmpBool

        if isGradeDownOnList:
            if currGrade=="6e":
                speedAdjust=1
            else:
                speedAdjust=0
            tmpBool=(self.minSpeedToSlice[currSpeedBumps][gradeDown][currShape] == 100)
            tmpBool=tmpBool or (self.minSpeedToSlice[currSpeedBumps][gradeDown][currShape] + speedAdjust <= self.minSpeedToSlice[currSpeedBumps][currGrade][currShape])
            sanity=sanity and tmpBool

        if isGradeUpOnList:
            if currGrade=="a":
                speedAdjust=1
            else:
                speedAdjust=0
            tmpBool=(self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] == 100)
            tmpBool=tmpBool or (self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] + speedAdjust <= self.minSpeedToSlice[currSpeedBumps][gradeUp][currShape])
            sanity=sanity and tmpBool
       
        return sanity

    def isSettingOnPartialList(self, iterateList, listPosition, speedBumps, grade, shape) -> bool:
        isOnList=False
        for x in range(0,listPosition+1):
            tmpBool=True
            tmpBool=tmpBool and (iterateList[x]["target"] == "minSpeedToSlice")
            tmpBool=tmpBool and (iterateList[x]["speedBumps"] == speedBumps)
            tmpBool=tmpBool and (iterateList[x]["grade"] == grade)
            if iterateList[x]["shape"] != "any":
                tmpBool=tmpBool and (iterateList[x]["shape"] == shape)
            isOnList=isOnList or tmpBool
            if isOnList:
                break
        return isOnList
            
