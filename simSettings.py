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
        self.snapshot="none"

        self.noHash={"iterateList":{} }

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
            
            "noHash" : self.noHash
            ,"general" : self.general
            ,"minInitialSpeed": self.minInitialSpeed
            ,"uncoverStatsLimit": self.uncoverStatsLimit
            ,"minSpeedToSlice": self.minSpeedToSlice
            ,"minSpeedToKeep": self.minSpeedToKeep
            ,"modStore": self.modStore
        }
        return settings

    def getAllButNoHash(self):
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
        assert(False) # outdated for now

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
                        self.iterateStep2(iteratedList)
                else:
                    self.iterateStep2(iteratedList)

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
 
    def iterateSaveToFiles(self, iterateList, iteratedList, outputPrefix, fileCut):
        assert(self.snapshot != "none")

        if fileCut>0:
            cutFileName="iteration_results/"+outputPrefix +"x" +str(self.fileCount)+".json"
            self.fileCount+=1
        else:
           cutFileName="iteration_results/"+outputPrefix+".json"
    
        header={}
        header["settingsSnapshot"] = self.snapshot
        header["snapshotHash"] = SimSettings.settingsHashOf(self.snapshot)
        header["snapshotFingerprint"] = SimSettings.settingsFingerprintOf(self.snapshot)
        header["iterateList"] = iterateList

        jobs={"header": header, "jobList": iteratedList }

        with open(cutFileName, "w") as fp:
            json.dump(jobs, fp)

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
        return SimSettings.settingsFingerprintOf(self.getAll())
        
    @staticmethod
    def settingsFingerprintOf(settings) -> str:
        fingerprint=""
        
        settingsCopy=json.loads(json.dumps(settings))   #fix for int to str change by json

        fingerprint+=str(settingsCopy["uncoverStatsLimit"]["e"]["square"])
        fingerprint+=str(settingsCopy["uncoverStatsLimit"]["d"]["square"])
        
        fingerprint+=str(settingsCopy["minInitialSpeed"]["e"]["square"])
        fingerprint+=str(settingsCopy["minInitialSpeed"]["d"]["square"])

        fingerprint+=str(settingsCopy["minSpeedToSlice"]["1"]["e"]["square"])

        fingerprint+=str(settingsCopy["minSpeedToSlice"]["1"]["d"]["square"])
        fingerprint+=str(settingsCopy["minSpeedToSlice"]["2"]["d"]["square"])

        fingerprint+=str(settingsCopy["minSpeedToSlice"]["1"]["c"]["square"])
        fingerprint+=str(settingsCopy["minSpeedToSlice"]["2"]["c"]["square"])
        fingerprint+=str(settingsCopy["minSpeedToSlice"]["3"]["c"]["square"])
     
        for grade in ["b", "a", "6e", "6d", "6c", "6b"]:
            for speedBumps in ["1", "2", "3", "4"]:
                fingerprint+=str(settingsCopy["minSpeedToSlice"][speedBumps][grade]["square"])
        
        return fingerprint

    def settingsHash(self) -> int:
        return SimSettings.settingsHashOf(self.getAllButNoHash())
    
    @staticmethod
    def settingsHashOf(settings) -> int:
        return binascii.crc32(bytes(json.dumps(settings), "utf-8"))
    
    def iterateSettingsByListQuick(self, iterateList, listPosition=0, iteratedList=[], complexityList=[], countBranchOnly=0, benchmarkPercent=0,
     outputPrefix="none", fileCut=0, sanityConstraint=1, lightweight=1):
 
        if not complexityList:
            assert(self.general["quickSDCCTForking"] == 1)
            assert(listPosition==0)
            self.calculateComplexity(iterateList, complexityList)
            self.iterationBranchesTotal=complexityList[0]
            self.iteratedBranches=0
            self.generatedSettings=0
            self.makeSnapshot()
            

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
                self.set(currentIteration["target"], x, grade=currentIteration["grade"], shape="square" , speedBumps=currentIteration["speedBumps"])  ## Ignore other shapes
                if self.iterateCheckSanityPartialQuick(iterateList, listPosition):
                    self.iterateSettingsByListQuick(iterateList, listPosition+1, iteratedList, complexityList, countBranchOnly, benchmarkPercent, outputPrefix, fileCut, sanityConstraint, lightweight)
                else:
                    if self.testlevel>9:
                        print("partial sanity branch cut, list pos:", listPosition, "branches cut:", complexityList[listPosition+1])
                    self.iteratedBranches+= complexityList[listPosition+1]

        #nope all on list has been iterated 
        else:
            self.iterationCount+= 1
            self.iteratedBranches+= 1

            # Because allready checked by partial sanity, last step is not partial but full   
            #assert(self.iterateCheckSanity() == True)
            
            #if (sanityConstraint==1) and not self.iterateCheckSanity() :
            #    pass

            #sanity provided by quick partial sanity
            
            self.generatedSettings+=1
            if (self.testlevel>0) and (self.iterationCount % 10000 == 0):
                #print(".", end="")
                pass

            if (self.testlevel>0) and (self.iterationCount % 1000 == 0):
                print("branches:", '{:,}'.format(self.iteratedBranches), "of", '{:,}'.format(self.iterationBranchesTotal), 
                "(", '{:,}'.format(self.iteratedBranches/self.iterationBranchesTotal*100) ,"% )", "valid settings produced", '{:,}'.format(self.generatedSettings) )
                
            if self.testlevel>20:
                input()

 
            if countBranchOnly>0 :
 
                if self.testlevel>20:
                    print(self.settingsFingerprint()," ", end="")
                    print(self.settingsHash())
                    print("fingerprint:",len(self.settingsFingerprint()), "settings:", len(json.dumps(self.getAll())))

                if (self.testlevel>0) and (self.generatedSettings % 10000 == 0):
                    #print("*", end="")
                    pass

            else:
            
                if (self.testlevel>0) and (self.generatedSettings % 1000 == 0):
                    #print("*", end="")
                    pass
                    
                if benchmarkPercent>0:
                    if (self.generatedSettings % (benchmarkPercent*100) == 0):
                        self.iterateStep2(iteratedList, iterateList, lightweight)
                else:
                    self.iterateStep2(iteratedList, iterateList, lightweight)


                if outputPrefix!="none" and fileCut>0:
                    if (self.generatedSettings % fileCut) == 0:
                        print("save")
                        self.iterateSaveToFiles(iterateList, iteratedList, outputPrefix, fileCut)
            
        #means original function call, and iterations done
        if listPosition==0: 
            if countBranchOnly>0:
                return self.generatedSettings
            elif outputPrefix!="none":
                self.iterateSaveToFiles(iterateList, iteratedList, outputPrefix, fileCut)
                return outputPrefix
            else:
                return iteratedList

    def iterateStep2(self, iteratedList, iterateList, lightweight):
        if lightweight==0:
            #settingsCopy=deepcopy(self.getAll())
            settingsCopy=json.loads(json.dumps(self.getAll()))
            iteratedList.append([self.generatedSettings, settingsCopy, self.settingsFingerprint(), self.settingsHash()])
        else:
            assert(self.general["quickSDCCTForking"] == 1)
            iteratedSettings=self.getIteratedSettingsOnly(iterateList)
            iteratedList.append([self.generatedSettings, iteratedSettings, self.settingsFingerprint(), self.settingsHash()])

            if self.testlevel > 99:
                with open("iteration_results/generated"+str(self.generatedSettings), "w") as fp:
                    json.dump(self.getAll(), fp)
                
                assert(False)


    def calculateComplexity(self, iterateList, complexityList):
        for baseLevel in range(0, len(iterateList)):
            complexity=1
            for level in range(baseLevel, len(iterateList)):
                complexity*= len(iterateList[level]["range"])
            complexityList.append(complexity)
        complexityList.append(1)

    def iterateCheckSanityPartialQuick(self, iterateList, listPosition) -> bool :

        sanity=True
        assert(self.general["quickSDCCTForking"] == 1)
        currShape="square"  

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
            tmpBool=(self.minSpeedToSlice[speedBumpsDown][currGrade][currShape] <= self.minSpeedToSlice[currSpeedBumps][currGrade][currShape])
            sanity=sanity and tmpBool

        if isSpeedBumpsUpOnList:
            tmpBool=(self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] <= self.minSpeedToSlice[speedBumpsUp][currGrade][currShape])
            sanity=sanity and tmpBool

        if isGradeDownOnList:
            if currGrade=="6e":
                speedAdjust=1
            else:
                speedAdjust=0

            tmpBool=(self.minSpeedToSlice[currSpeedBumps][gradeDown][currShape] + speedAdjust <= self.minSpeedToSlice[currSpeedBumps][currGrade][currShape])
            sanity=sanity and tmpBool

        if isGradeUpOnList:
            if currGrade=="a":
                speedAdjust=1
            else:
                speedAdjust=0

            tmpBool=(self.minSpeedToSlice[currSpeedBumps][currGrade][currShape] + speedAdjust <= self.minSpeedToSlice[currSpeedBumps][gradeUp][currShape])
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

    def makeSnapshot(self):
        self.snapshot=deepcopy(self.getAllButNoHash())      
 
    def getIteratedSettingsOnly(self, iterateList) -> dict :
        settings={}

        for iteration in iterateList:
            target=iteration["target"]
            grade=iteration["grade"]
            shape=iteration["shape"]
            speedBumps=iteration["speedBumps"]

            assert(grade != "any")
            if shape == "any":
                shape = "square"
            assert(shape == "square")
            assert(speedBumps != "any")

            if target in ["uncoverStatsLimit", "minInitialSpeed"]:
                if target not in settings.keys():
                    settings[target] = {}
                
                if grade not in settings[target].keys():
                    settings[target][grade]={}

                if target == "uncoverStatsLimit":
                    settings[target][grade][shape] = self.uncoverStatsLimit[grade][shape]
                elif target == "minInitialSpeed":
                    settings[target][grade][shape] = self.minInitialSpeed[grade][shape]
                else:
                    assert(False)

            if target in ["minSpeedToKeep"]:
                assert(False)

            if target in ["minSpeedToSlice"]:
                if target not in settings.keys():
                    settings[target] = {}                

                if speedBumps not in settings[target].keys():
                    settings[target][speedBumps] = {}

                if grade not in settings[target][speedBumps].keys():
                    settings[target][speedBumps][grade] = {}
                
                settings[target][speedBumps][grade][shape] = self.minSpeedToSlice[speedBumps][grade][shape]

        return settings

    @staticmethod
    def mergeSettings(base, changes):
        for a in changes:
            if a in ["uncoverStatsLimit", "minInitialSpeed"]:  ## depth 3 dict
                for b in changes[a]:
                    for c in changes[a][b]:
                        base[a][b][c] = changes[a][b][c]
                        
            elif a in ["minSpeedToSlice"]:                     ## depth 4 dict
                for b in changes[a]:
                    for c in changes[a][b]:
                        for d in changes[a][b][c]:
                            base[a][b][c][d] = changes[a][b][c][d]

            else:
                assert(False)