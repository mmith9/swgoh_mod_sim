
from modsimulation import ModSimulation
from modAnalysis import *
from copy import deepcopy
from modStore import *


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

settings={"resources" : resources, "general" : general, "minInitialSpeed": minInitialSpeed, "minLev12Speed":minLev12Speed, "minSpeedIfBumpMissed":minSpeedIfBumpMissed}

baseSettings=deepcopy(settings)


baseSettings["general"]["greyMaxInitialStats"]=4

for shape in Mod.shapes:
    baseSettings["minInitialSpeed"]["e"][shape]=6
    pass

#baseSettings["minInitialSpeed"]["e"]["triangle"]=6

for shape in Mod.shapes:
    #baseSettings["minInitialSpeed"]["d"][shape]=3
    baseSettings["minLev12Speed"]["d"][shape]=7
    pass

for shape in Mod.shapes:
    #baseSettings["minInitialSpeed"]["c"][shape]=3
    baseSettings["minLev12Speed"]["c"][shape]=9
    baseSettings["minSpeedIfBumpMissed"]["c"][shape]=9
    pass

for shape in Mod.shapes:
    #baseSettings["minInitialSpeed"]["b"][shape]=3
    #baseSettings["minLev12Speed"]["b"][shape]=14
    baseSettings["minSpeedIfBumpMissed"]["b"][shape]=10
    pass

for shape in Mod.shapes:
#    baseSettings["minInitialSpeed"]["a"][shape]=3
#    baseSettings["minSpeedIfBumpMissed"]["a"][shape]=11
    pass

base=ModSimulation()
baseOutput = base.walkIt(baseSettings)
baseEnergyCost=-baseOutput.avgEnergyChange
baseCreditCost=-baseOutput.avgCreditsChange
print(baseEnergyCost)
print(baseCreditCost)

baseDailyFactor=resources["dailyEnergy"]/baseEnergyCost

baseBudget=resources["dailyCredits"]-baseCreditCost*baseDailyFactor
print("budget for mods",baseBudget)

modStore=ModStore()
wishlist=[
        {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
    ]
boughtItems=modStore.modShopping(baseBudget, wishlist)

item=boughtItems[0]
print(item)

mod=item["mod"]
prob=item["dailyProbability"]
cost=item["dailyCreditCost"]

base.walkBoughtMod(item["dailyProbability"]/baseDailyFactor, item["mod"])

base.creditChange(1 / baseDailyFactor, -item["dailyCreditCost"])



########################
compareSettings=deepcopy(settings)

compareSettings["general"]["greyMaxInitialStats"]=2

for shape in Mod.shapes:
    compareSettings["minInitialSpeed"]["e"][shape]=5
    pass

for shape in Mod.shapes:
    #compareSettings["minInitialSpeed"]["d"][shape]=3
    compareSettings["minLev12Speed"]["d"][shape]=7
    #compareSettings["minSpeedIfBumpMissed"]["d"][shape]=7
    pass

for shape in Mod.shapes:
    #compareSettings["minInitialSpeed"]["c"][shape]=3
    #compareSettings["minLev12Speed"]["c"][shape]=11
    compareSettings["minSpeedIfBumpMissed"]["c"][shape]=9
    pass

for shape in Mod.shapes:
    #compareSettings["minInitialSpeed"]["b"][shape]=3
    #compareSettings["minLev12Speed"]["b"][shape]=13
    compareSettings["minSpeedIfBumpMissed"]["b"][shape]=10
    pass

for shape in Mod.shapes:
#    compareSettings["minInitialSpeed"]["a"][shape]=3
#    compareSettings["minSpeedIfBumpMissed"]["a"][shape]=11
    pass

compare=ModSimulation()
compareOutput=compare.walkIt(compareSettings)
compareEnergyCost=-compareOutput.avgEnergyChange
compareCreditCost=-compareOutput.avgCreditsChange

print(compareEnergyCost)
print(compareCreditCost)

compareDailyFactor=resources["dailyEnergy"]/compareEnergyCost

compareBudget=resources["dailyCredits"]-compareCreditCost*compareDailyFactor
print("budget for mods",compareBudget)

modStore=ModStore()
wishlist=[
        {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
    ]
boughtItems=modStore.modShopping(compareBudget, wishlist)

item=boughtItems[0]
print(item)

mod=item["mod"]
prob=item["dailyProbability"]
cost=item["dailyCreditCost"]

compare.walkBoughtMod(item["dailyProbability"]/compareDailyFactor, item["mod"])

print(compareOutput.avgCreditsChange)
compare.creditChange(1 / compareDailyFactor, -item["dailyCreditCost"])

print(compareEnergyCost)
print(compareOutput.avgCreditsChange)
##################################################

energyRatio=baseEnergyCost/compareEnergyCost

print("speed distribution % change")
print("all compare values are multiplied by base/compare energy cost which is",baseEnergyCost,"/",compareEnergyCost,"=", energyRatio)
for x in range(0,32):
    base=baseOutput.speedDistribution[x]
    cmp=compareOutput.speedDistribution[x]
    if (cmp!=0):
        print (x,cmp*energyRatio*100/base)
    else:
        print("div0")

print("base daily credits",baseOutput.avgCreditsChange*baseDailyFactor)
print("compare daily credits",compareOutput.avgCreditsChange*compareDailyFactor)

baseOutput.calcScores(baseDailyFactor)
compareOutput.calcScores(compareDailyFactor)


#baseSpeedValue=Distribution.value(baseOutput.speedDistribution)
#compareSpeedValue=Distribution.value(compareOutput.speedDistribution,energyRatio)

#baseFertilityValue=Distribution.value(baseOutput.speedPerSpeedUpDistribution[4])
#compareFertilityValue=Distribution.value(compareOutput.speedPerSpeedUpDistribution[4],energyRatio)

print("base speed   ",baseOutput.speedValue)
print("compare speed",compareOutput.speedValue)
print("cmp/base     ",compareOutput.divideValues(compareOutput.speedValue,baseOutput.speedValue))
print()
print("base fertility   ",baseOutput.fertility)
print("compare fertility",compareOutput.fertility)
print("cmp/base         ",compareOutput.divideValues(compareOutput.fertility,baseOutput.fertility))
print()
print("base tilt   ",baseOutput.rltilt)
print("compare tilt", compareOutput.rltilt)
print("base tga    ", baseOutput.targetability)
print("compare tga ", compareOutput.targetability)
print("base speed arrows:", baseOutput.speedArrowProbability*baseDailyFactor)
print("compare speed arrows:", compareOutput.speedArrowProbability*compareDailyFactor)

print(returnValueHigh(baseOutput))
