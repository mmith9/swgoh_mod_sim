
from mod import Mod
from budget import Budget

class ModAnalysis:
        
    def __init__(self):

        self.budget=Budget()

        
        self.rltilt="undefined"
        self.targetability="undefined"
        self.speedValue="undefined"

        self.speedDistribution=[0 for x in range(0,32)]

        self.speedArrowProbability=0
        
        shapes=Mod.getShapes()
        self.shapeDistribution={}
        for shape in shapes:
            self.shapeDistribution[shape]=0
        
        self.speedPerShapeDistribution={}
        for shape in shapes:
            self.speedPerShapeDistribution[shape]=[0 for x in range(0,32)]
        
        self.cdTriangleSpeedDistribution=[0 for x in range(0,32)]
        
        self.speedPerSpeedUpDistribution={}
        for SpeedUp in range(0,6):
            self.speedPerSpeedUpDistribution[SpeedUp]=[0 for x in range(0,32)]
        
        primaries=Mod.getPrimaries()
        self.primaryPerShapeDistribution={}
        for shape in shapes:
            self.primaryPerShapeDistribution[shape]={}
            for primary in primaries[shape]:
                self.primaryPerShapeDistribution[shape][primary]=0

    def analyzeModList(self, modList):
        for mod in modList:
            self.analyzeMod(1, mod)
    
    def analyzeMod(self, levelProbability, mod):
            primary=mod.getPrimary()
            secondary=mod.getSecondary()
            shape=mod.getShape()
            #modSet=mod.getSet()
            if shape=="arrow":
                if primary=="speed":
                    self.speedArrowProbability+=levelProbability
            else:
                if "speed" in secondary:
                    speed=secondary["speed"][1]
                    speedUps=secondary["speed"][0]
                else:
                    speed=0
                    speedUps=0
                            
                self.speedDistribution[speed]+=levelProbability 
                self.speedPerShapeDistribution[shape][speed]+=levelProbability
                if shape=="triangle" and primary=="crit dmg":
                    self.cdTriangleSpeedDistribution[speed]+=levelProbability
                self.speedPerSpeedUpDistribution[speedUps][speed]+=levelProbability
       
    def calcScores(self, multiplier=1):

        self.speedValue=self.value(self.speedDistribution, multiplier)
                
        self.squaresValue=self.value(self.speedPerShapeDistribution["square"])
        self.diamondsValue=self.value(self.speedPerShapeDistribution["diamond"])
        self.circlesValue=self.value(self.speedPerShapeDistribution["circle"])
        self.crossesValue=self.value(self.speedPerShapeDistribution["cross"])
        self.trianglesValue=self.value(self.speedPerShapeDistribution["triangle"])
        
        self.r=self.squaresValue
        self.r=self.addValues(self.r, self.diamondsValue)
        self.r=self.addValues(self.r, self.circlesValue)
        self.l=self.crossesValue
        self.l=self.addValues(self.l, self.trianglesValue)
        self.rltilt=self.divideValues(self.l, self.r)

        self.targetability=self.divideValues(self.value(self.cdTriangleSpeedDistribution, multiplier),self.speedValue)

        self.rltilt=self.multiplyValueByX(self.rltilt,100*3/2)
        self.targetability=self.multiplyValueByX(self.targetability,100)

    def getScores(self):
        scores={
        "speedValue":self.speedValue,
                
        "squaresValue":self.squaresValue,
        "diamondsValue": self.diamondsValue,
        "circlesValue": self.circlesValue,
        "crossesValue": self.crossesValue,
        "trianglesValue": self.trianglesValue,

        "rltilt": self.rltilt,
        "targetability": self.targetability,

        "speedDistribution": self.speedDistribution
        
        }
        
        return scores


        # print(self.squaresValue)
        # print(self.diamondsValue)

        
        # print(self.trianglesValue)
        # print(self.rltilt)
        # print(self.targetability)
        # print()
 
    def value(self,dist, multiplier=1):
        values={"high":0, "mid":0, "low":0, "Elisa":0, "ElisaM14":0}
        x=1
        steps={}
        factors={}
        for value in values:
            if value in ["high","mid","low"]:
                steps[value]=4**(1/(1+x))   # root 2 of 4, root 3 of 4, root 4 of 4
                factors[value]=1
                x+=1

        for x in range(0,32):
            for value in values:
                if value in ["high","mid","low"]:
                    values[value]+=dist[x] *factors[value] *multiplier
                    factors[value]*=steps[value]
                if value == "Elisa" and x>9:
                    values["Elisa"]+=dist[x] * ((x-9)**3) *multiplier
                if value == "ElisaM14" and x>14:
                    values["ElisaM14"]+=dist[x] * ((x-14)**3) *multiplier
                
        return values

    def divideValues(self,value1,value2):
        div={}
        for value in value1:
            if value2[value]!=0:
                div[value]=value1[value]/value2[value]
            else:
                div[value]="div0"
        return div

    def addValues(self,value1, value2):
        sum={}
        for value in value1:
            sum[value]=value1[value]+value2[value]
        return sum

    def multiplyValueByX(self,values, multiplier):
        mlt={}
        for value in values:
            if type(values[value]) == int or type(values[value]) == float:
                mlt[value]=values[value]*multiplier
            else:
                mlt[value]=values[value]
        return mlt

    def addAnalysis(self, analysisToAdd, multiplier=1):
        self.speedArrowProbability+= analysisToAdd.speedArrowProbability *multiplier

        for speed in range (0,32):
            self.speedDistribution[speed]+= analysisToAdd.speedDistribution[speed] *multiplier
            self.cdTriangleSpeedDistribution[speed]+= analysisToAdd.cdTriangleSpeedDistribution[speed] *multiplier
        
        shapes=Mod.getShapes()
        for shape in shapes:
            self.shapeDistribution[shape]+= analysisToAdd.shapeDistribution[shape] *multiplier

        for shape in shapes:
            for speed in range(0,32):
                self.speedPerShapeDistribution[shape][speed]+= analysisToAdd.speedPerShapeDistribution[shape][speed] *multiplier
        
        for speedUp in range(0,6):
            for speed in range (0,32):
                self.speedPerSpeedUpDistribution[speedUp][speed]+= analysisToAdd.speedPerSpeedUpDistribution[speedUp][speed] *multiplier
        
        primaries=Mod.getPrimaries()

        for shape in shapes:
            for primary in primaries[shape]:
                self.primaryPerShapeDistribution[shape][primary]+= analysisToAdd.primaryPerShapeDistribution[shape][primary] *multiplier


def returnValueHigh(analysis:ModAnalysis):
    return analysis.speedValue["high"]

def returnValueMid(analysis:ModAnalysis):
    return analysis.speedValue["mid"]

def returnValueLow(analysis:ModAnalysis):
    return analysis.speedValue["low"]

def returnValueElisa(analysis:ModAnalysis):
    return analysis.speedValue["Elisa"]

def returnValueElisaM14(analysis:ModAnalysis):
    return analysis.speedValue["ElisaM14"]

