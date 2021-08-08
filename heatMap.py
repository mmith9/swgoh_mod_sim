from copy import deepcopy
from modAnalysis import ModAnalysis
from mod import Mod



class HeatMap:

    def __init__(self) -> None:
        self.testlevel=0
        self.version="singleSim"
        self.activeMarkers=[]
        self.HEATmap={}

    def addMarker(self, levelProbability, mod:Mod):
        if self.isHeatApplicable(levelProbability, mod):
            marker=HeatMap.makeHeatMarker(levelProbability, mod)
            assert(self.isMarkerAllreadyActive(marker) == False)
            self.activeMarkers.append(marker)
        else:
            pass

    def stripMarker(self, levelProbability, mod:Mod):
        assert(self.isHeatApplicable(levelProbability, mod))
        sameMarker=HeatMap.makeHeatMarker(levelProbability, mod)
        assert(self.activeMarkers)
        oldMarker=self.activeMarkers.pop()
        assert(HeatMap.areMarkersForSameMod(oldMarker, sameMarker))

    def getSubAnalysisFor(self, levelProbability, mod:Mod) -> dict:  ## RETURNS NORMALIZED DISTRIBUTION
        subAnalysis= False

        if self.isHeatApplicable(levelProbability, mod):
            marker=HeatMap.makeHeatMarker(levelProbability, mod)
            subAnalysis= self.getHeatVortex(marker)
            
            if subAnalysis and self.testlevel > 95:
                tmpSum=0
                for x in range (0,32):
                    tmpSum+= subAnalysis["dist"][x]
                print(" subanalysis sum", tmpSum ," for ", marker)
        return subAnalysis
            
    def analyzeMod(self, modlevelProbability, mod:Mod):
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


    def addHeatVortexToActiveMarkers(self, modLevelProbability, modVortex):
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
            for key in marker.keys():
                if key != "levelProbability" and key!="vortex" :
                    value=marker[key]
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
            for key in marker.keys():
                if key != "levelProbability" and key!="vortex" :
                    value=marker[key]

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
        isApplicable=isApplicable and mod.level >= 12
        isApplicable=isApplicable and mod.grade in [ "d", "c","b","a", "6e", "6d", "6c"]
        #isApplicable=isApplicable and speedBumps in [3,4]
        #isApplicable=isApplicable and speed in range(speedBumps*3 , speedBumps*6 -1)
        return isApplicable

    @staticmethod
    def makeHeatMarker(levelProbability, mod:Mod) -> dict:
        marker={}
        marker["levelProbability"]=levelProbability
        marker["vortex"]=False
        marker["grade"]=mod.grade
        marker["shape"]=mod.shape
        marker["level"]=mod.level
        marker["primary"]=mod.primary
        marker["speedBumps"]=mod.secondary["speed"][0]
        marker["speed"]=mod.secondary["speed"][1]
        return marker

    @staticmethod
    def areMarkersIdentical(marker1, marker2) -> bool:
        tmpBool=True
        for x in marker1:
            tmpBool= tmpBool and (marker1[x] == marker2[x])
        return tmpBool

    @staticmethod
    def areMarkersForSameMod(marker1, marker2) -> bool:
        tmpBool=True
        for x in marker1:
            if x!= "levelProbability" and x!="vortex" :

                tmpBool= tmpBool and (marker1[x] == marker2[x])
        return tmpBool


