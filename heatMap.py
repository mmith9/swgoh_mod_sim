from copy import deepcopy
from modAnalysis import ModAnalysis
from mod import Mod



class HeatMap:

    def __init__(self) -> None:
        self.testlevel=0
        self.version="multiSim"
        self.activeMarkers=[]
        self.HEATmap={}

    def reset(self):
        self.activeMarkers=[]
        self.HEATmap={}

    def addMarker(self, levelProbability, mod:Mod, simSettings={}):
        if self.version == "multiSim" and not simSettings:
            assert(False)

        if True: #self.version == "singleSim":
            if self.isHeatApplicable(levelProbability, mod):
                marker=self.makeHeatMarker(levelProbability, mod, simSettings)
                assert(self.isMarkerAllreadyActive(marker) == False)
                self.activeMarkers.append(marker)

#                print("DROPPING MARKER")
#                print(marker)
            else:
                pass
        else:
            assert(False)


    def stripMarker(self, levelProbability, mod:Mod, simSettings={}):
        if self.version == "multiSim" and not simSettings:
            assert(False)
       
        assert(self.isHeatApplicable(levelProbability, mod))
        sameMarker=self.makeHeatMarker(levelProbability, mod, simSettings)
        assert(self.activeMarkers)
        oldMarker=self.activeMarkers.pop()
        assert(HeatMap.areMarkersForSameMod(oldMarker, sameMarker))
    
    def getSubAnalysisFor(self, levelProbability, mod:Mod, simSettings={}) -> dict:  ## RETURNS NORMALIZED DISTRIBUTION
        if self.version == "multiSim" and not simSettings:
            assert(False)

        subAnalysis= False
        

        if self.isHeatApplicable(levelProbability, mod):
            marker=self.makeHeatMarker(levelProbability, mod, simSettings)
            subAnalysis= self.getHeatVortex(marker)
            
            if subAnalysis and self.testlevel > 95:
                tmpSum=0
                for x in range (0,32):
                    tmpSum+= subAnalysis["dist"][x]
                print(" subanalysis sum", tmpSum ," for ", marker)
        return subAnalysis
                   
    def analyzeMod(self, modlevelProbability, mod:Mod, simSettings={}):
        for marker in self.activeMarkers:

            modSpeed=mod.secondary["speed"][1]
            markerVortex= self.getOrMakeHeatVortex(marker)
            markerProbability= marker["levelProbability"]

            markerVortex["dist"][modSpeed]+= modlevelProbability / markerProbability  
    
    def analyzeBudgetChange(self, levelProbability, change):
        for marker in self.activeMarkers:

            markerVortex=self.getOrMakeHeatVortex(marker)
            markerProbability= marker["levelProbability"]
            for what in change:
                if what in markerVortex["costs"].keys():
                    markerVortex["costs"][what]+= change[what] * levelProbability / markerProbability
                else:
                    markerVortex["costs"][what] = change[what] * levelProbability / markerProbability


    def addHeatVortexToActiveMarkers(self, modLevelProbability, modVortex, simSettings={}):
        for marker in self.activeMarkers:

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
        speedBumps=mod.secondary["speed"][0]
        speed=mod.secondary["speed"][1]
        isApplicable=True
        #isApplicable=isApplicable and mod.level >= 12
        #isApplicable=isApplicable and mod.grade in [ "d", "c","b","a", "6e", "6d", "6c"]
        #isApplicable=isApplicable and speedBumps in [3,4]
        #isApplicable=isApplicable and speed in range(speedBumps*3 , speedBumps*6 -1)
        return isApplicable
 
    def makeHeatMarker(self, levelProbability, mod:Mod, simSettings={}) -> dict:
        if self.version == "multiSim" and not simSettings:
                assert(False)

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
        
        if self.version == "singleSim":
            return marker
        elif self.version == "multiSim":
            multiSimMarkers= HeatMap.selectApplicableIterates(mod, simSettings)

            for iteration in multiSimMarkers:
                key=iteration["grade"]+iteration["speedBumps"]
                value=simSettings["minSpeedToSlice"][iteration["speedBumps"]][iteration["grade"]]["square"]
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
    @staticmethod
    def selectApplicableIterates(mod:Mod, simSettings:dict)-> list:
        
        if not simSettings:
            assert(False)
        
        iterateList=simSettings["general"]["iterateList"]
        applicables=[]

        for iteration in iterateList:
           # print(iteration)
            if iteration["target"] == "minSpeedToSlice":
                tmpBool=True
                tmpBool=tmpBool and (Mod.allGrades.index(mod.grade) < Mod.allGrades.index(iteration["grade"]) or (mod.level < 15 and mod.grade == iteration["grade"]))
                tmpBool=tmpBool and (mod.secondary["speed"][0] <= int(iteration["speedBumps"]))

                if tmpBool:
                    applicables.append({"grade": iteration["grade"], "speedBumps":HeatMap.speedBumpsStr(iteration["speedBumps"]) })

            else:
                pass #ignore other iterables
        
#        print(applicables)
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