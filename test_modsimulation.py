
from modsimulation import ModSimulation
from modAnalysis import *
from copy import deepcopy
from mod import *
from simSettings import *

baseSettings=SimSettings()
base=ModSimulation()

baseSettings.set("uncoverStatsLimit", 4, grade="e")
baseSettings.set("minSpeedToKeep", 0)
baseSettings.set("minSpeedToSlice", 100)
baseSettings.set("minSpeedToSlice", 0 , grade="e", speedBumps=1)
baseSettings.set("minSpeedToSlice", 0 , grade="d", speedBumps=2)
baseSettings.set("minSpeedToSlice", 0 , grade="c", speedBumps=3)
baseSettings.set("minSpeedToSlice", 0 , grade="b", speedBumps=4)


#print(baseSettings.getAll()["minSpeedToSlice"])


baseOutput = base.walkIt(baseSettings.getAll())

baseEnergyCost=-baseOutput.avgEnergyChange
baseCreditCost=-baseOutput.avgCreditsChange

print("bs full costs", baseOutput.costs)
baseDailyFactor=baseOutput.costs["dailyFactor"]


########################
compareSettings=SimSettings()
compare=ModSimulation()

compareSettings.set("uncoverStatsLimit", 3, grade="e")
compareSettings.set("minInitialSpeed", 5, grade="e")
compareSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])
compareSettings.set("minSpeedToSlice", 5 , grade="e")
compareSettings.set("minSpeedToSlice", 8 , grade="d")
compareSettings.set("minSpeedToSlice", 10 , grade="c")
compareSettings.set("minSpeedToSlice", 12 , grade="b")



compareOutput=compare.walkIt(compareSettings.getAll())

compareEnergyCost=-compareOutput.avgEnergyChange
compareCreditCost=-compareOutput.avgCreditsChange
compareDailyFactor=compareOutput.costs["dailyFactor"]

print("bs full costs", compareOutput.costs)


print(compareEnergyCost)
print(compareOutput.avgCreditsChange)
##################################################

energyRatio=baseEnergyCost/compareEnergyCost

print("speed distribution % change")
print("all compare values are multiplied by base/compare energy cost which is",baseEnergyCost,"/",compareEnergyCost,"=", energyRatio)
for x in range(0,32):
    base=baseOutput.speedDistribution[x]
    cmp=compareOutput.speedDistribution[x]
    if (base!=0):
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

