from modAnalysis import ModAnalysis
from mod import Mod

class HeatMap:

    def __init__(self, heat={"mode":"singleSim", "iterateList":False}) -> None:

        self.testlevel=0
        self.mode=heat["mode"]
        self.activeMarkers=[]
        self.HEATmap={}
        self.iterateList=heat["iterateList"]
        self.simSettings=False

        self.precalculateThings=True

        if (self.precalculateThings):
            self.precalcGetApplicableIterates()

    def supplySettings(self, simSettings):
        self.simSettings=simSettings

    def reset(self):
        self.activeMarkers=[]
        self.HEATmap={}

    def addMarker(self, levelProbability, mod:Mod):
        if self.isHeatApplicable(levelProbability, mod):
            marker=self.makeHeatMarker(levelProbability, mod)
            assert(self.isMarkerAllreadyActive(marker) == False)
            self.activeMarkers.append(marker)

    def stripMarker(self, levelProbability, mod:Mod):
        #assert(self.isHeatApplicable(levelProbability, mod))
        #sameMarker=self.makeHeatMarker(levelProbability, mod)
        assert(self.activeMarkers)
        oldMarker=self.activeMarkers.pop()
        #assert(HeatMap.areMarkersForSameMod(oldMarker, sameMarker))
        if self.activeMarkers:
            self.addHeatVortexToLastActiveMarker(levelProbability, oldMarker["vortex"])

    
    def getSubAnalysisFor(self, levelProbability, mod:Mod) -> dict:  ## RETURNS NORMALIZED DISTRIBUTION
        subAnalysis= False
        if self.isHeatApplicable(levelProbability, mod):
            marker=self.makeHeatMarker(levelProbability, mod)
            subAnalysis= self.getHeatVortex(marker)
            
            if subAnalysis and self.testlevel > 95:
                tmpSum=0
                for x in range (0,32):
                    tmpSum+= subAnalysis["dist"][x]
                print(" subanalysis sum", tmpSum ," for ", marker)
        return subAnalysis
                   
    def analyzeMod(self, modlevelProbability, mod:Mod):
        if self.activeMarkers:
            marker=self.activeMarkers[-1]

        #for marker in self.activeMarkers:

            modSpeed=mod.secondary["speed"][1]
            markerVortex= self.getOrMakeHeatVortex(marker)
            markerProbability= marker["levelProbability"]

            markerVortex["dist"][modSpeed]+= modlevelProbability / markerProbability  
    
    def analyzeBudgetChange(self, levelProbability, change):
        if self.activeMarkers:
            marker=self.activeMarkers[-1]

        #for marker in self.activeMarkers:

            markerVortex=self.getOrMakeHeatVortex(marker)
            markerProbability= marker["levelProbability"]
            for what in change:
                if what in markerVortex["costs"].keys():
                    markerVortex["costs"][what]+= change[what] * levelProbability / markerProbability
                else:
                    markerVortex["costs"][what] = change[what] * levelProbability / markerProbability

    def addHeatVortexToLastActiveMarker(self, modLevelProbability, modVortex):
        if self.activeMarkers:
            marker=self.activeMarkers[-1]

        #for marker in self.activeMarkers:

            markerVortex=self.getOrMakeHeatVortex(marker)
            markerProbability= marker["levelProbability"]

            for speed in range(0,32):
                markerVortex["dist"][speed] += modVortex["dist"][speed] * modLevelProbability / markerProbability

            for what in modVortex["costs"]:
                if what in markerVortex["costs"].keys():
                    markerVortex["costs"][what]+= modVortex["costs"][what] * modLevelProbability / markerProbability
                else:
                    markerVortex["costs"][what] = modVortex["costs"][what] * modLevelProbability / markerProbability
        
    def getHeatVortex(self, marker):
        if marker["vortex"]:
            return marker["vortex"]
        else:
            cursor=self.HEATmap
            for key in marker["mapKeys"].keys():
                value=marker["mapKeys"][key]
                if value in cursor.keys():
                    cursor=cursor[value]
                else:
                    cursor=False
                    break
            marker["vortex"]=cursor
            return cursor
                
    def getOrMakeHeatVortex(self, marker):
        if marker["vortex"]:
            return marker["vortex"]
        else:
            cursor=self.HEATmap
            for key in marker["mapKeys"].keys():
                value=marker["mapKeys"][key]
                if value not in cursor.keys():
                    cursor[value]= {}
                cursor=cursor[value]

            if "dist" not in cursor.keys():
                cursor["dist"]=[0 for x in range(0,32)]
                cursor["costs"]={}

            marker["vortex"]=cursor
            return cursor

    def isMarkerAllreadyActive(self, markerToCheck) -> bool:
        isOnList=False
        for marker in self.activeMarkers:
            if HeatMap.areMarkersForSameMod(marker, markerToCheck):
                isOnList=True
                break
        return isOnList

    def heatFunction(self, levelProbability, mod:Mod, analysis:ModAnalysis, functionToHeat):
        assert(False)
        if self.isHeatApplicable(levelProbability, mod):
            vortex=self.getSubAnalysisFor(levelProbability, mod)
            if vortex:
                analysis.addHeatVortex(levelProbability, mod, vortex)
                self.addHeatVortexToActiveMarkers(levelProbability, vortex)
            else:
                self.addMarker(levelProbability, mod)
                if self.testlevel>100:
                    print(self.activeMarkers)
               
                functionToHeat(levelProbability, mod)            
                self.stripMarker(levelProbability, mod)

        else:
            functionToHeat(levelProbability, mod)

    @staticmethod
    def isHeatApplicable(levelProbability, mod:Mod) -> bool:
        #speedBumps=mod.secondary["speed"][0]
        #speed=mod.secondary["speed"][1]
        isApplicable=True
        #isApplicable=isApplicable and mod.level >= 12
        #isApplicable=isApplicable and mod.grade in [ "d", "c","b","a", "6e", "6d", "6c"]
        #isApplicable=isApplicable and speedBumps in [3,4]
        #isApplicable=isApplicable and speed in range(speedBumps*3 , speedBumps*6 -1)
        return isApplicable
 
    def makeHeatMarker(self, levelProbability, mod:Mod) -> dict:

        marker={}
        marker["levelProbability"]=levelProbability
        marker["vortex"]=False
        marker["mapKeys"]={}

        marker["mapKeys"]["grade"]=mod.grade
        marker["mapKeys"]["shape"]=mod.shape
        marker["mapKeys"]["level"]=mod.level
        marker["mapKeys"]["primary"]=mod.primary
        marker["mapKeys"]["speedBumps"]=mod.secondary["speed"][0]
        marker["mapKeys"]["speed"]=mod.secondary["speed"][1]
        
        #print(self.mode)

        if self.mode == "singleSim":
            return marker
        elif self.mode == "multiSim":
            multiSimMarkers= self.getApplicableIterates(mod)
            #print(multiSimMarkers)
            assert(self.simSettings)
            for iteration in multiSimMarkers:
                key=iteration["grade"]+iteration["speedBumps"]
                value=self.simSettings["minSpeedToSlice"][iteration["speedBumps"]][iteration["grade"]]["square"]
                marker["mapKeys"][key] = value

            return marker
        else:
            assert(False)

    @staticmethod
    def areMarkersIdentical(marker1, marker2) -> bool:
        assert(False)
        tmpBool=True
        for x in marker1:
            tmpBool= tmpBool and (marker1[x] == marker2[x])
        return tmpBool

    @staticmethod
    def areMarkersForSameMod(marker1, marker2) -> bool:
        tmpBool=True
        for x in marker1["mapKeys"]:
            tmpBool= tmpBool and (marker1["mapKeys"][x] == marker2["mapKeys"][x])
        return tmpBool

    
    #uncover stat limit and min initial speed not covered!
    #heat has to be applied DOWNSTREAM of those!
    
    def getApplicableIterates(self, mod:Mod)-> list:
        assert(self.simSettings)
        
        if self.precalculateThings:
            applicables=self.applicableIteratesMap[mod.grade][mod.secondary["speed"][0]][mod.level]
        else:
            applicables=[]
            for iteration in self.iterateList:
            # print(iteration)
                if iteration["target"] == "minSpeedToSlice":
                    tmpBool=True
                    tmpBool=tmpBool and (Mod.allGrades.index(mod.grade) < Mod.allGrades.index(iteration["grade"]) or (mod.level < 15 and mod.grade == iteration["grade"]))
                    tmpBool=tmpBool and (mod.secondary["speed"][0] <= int(iteration["speedBumps"]))

                    if tmpBool:
                        applicables.append({"grade": iteration["grade"], "speedBumps":HeatMap.speedBumpsStr(iteration["speedBumps"]) })

                else:
                    pass #ignore other iterables
        
        #print(mod.grade, mod.level, mod.secondary["speed"])
        
        return applicables

    @staticmethod
    def speedBumpsStr(speedBumps):

        if type(speedBumps) is int:
            if speedBumps==0:
                speedBumps="0"
            elif speedBumps==1:
                speedBumps="1"
            elif speedBumps==2:
                speedBumps="2"
            elif speedBumps==3:
                speedBumps="3"
            elif speedBumps==4:
                speedBumps="4"
            elif speedBumps==5:
                speedBumps="5"
        return speedBumps


    def precalcGetApplicableIterates(self):
        self.applicableIteratesMap={}

        for grade in Mod.allGrades:
            self.applicableIteratesMap[grade]={}

            for speedBumps in range(0,6):
                self.applicableIteratesMap[grade][speedBumps]={}
                
                for level in [1,3,6,9,12,15]:
                    self.applicableIteratesMap[grade][speedBumps][level]=[]

                    #optimize for below checks
                    if level>1 and level<15:
                        self.applicableIteratesMap[grade][speedBumps][level] = self.applicableIteratesMap[grade][speedBumps][1] 
                    else:
                        for iteration in self.iterateList:
                            # print(iteration)
                            if iteration["target"] == "minSpeedToSlice":
                                tmpBool=True
                                tmpBool=tmpBool and (Mod.allGrades.index(grade) < Mod.allGrades.index(iteration["grade"]) or (level < 15 and grade == iteration["grade"]))
                                tmpBool=tmpBool and (speedBumps <= int(iteration["speedBumps"]))

                                if tmpBool:
                                    self.applicableIteratesMap[grade][speedBumps][level].append({"grade": iteration["grade"], "speedBumps":HeatMap.speedBumpsStr(iteration["speedBumps"]) })

                            else:
                                pass #ignore other iterables

            




