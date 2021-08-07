
import modsimulation
from modAnalysis import *
from copy import deepcopy
from mod import *
from simSettings import *

baseSettings=SimSettings()
base=modsimulation.ModSimulation()

# baseSettings.set("uncoverStatsLimit", 4, grade="e")
# baseSettings.set("minSpeedToKeep", 0)
# baseSettings.set("minSpeedToSlice", 100)
# baseSettings.set("minSpeedToSlice", 0 , grade="e", speedBumps=1)
# baseSettings.set("minSpeedToSlice", 0 , grade="d", speedBumps=2)
# baseSettings.set("minSpeedToSlice", 0 , grade="c", speedBumps=3)
# baseSettings.set("minSpeedToSlice", 0 , grade="b", speedBumps=4)

baseSettings.set("uncoverStatsLimit", 2, grade="e")
baseSettings.set("minInitialSpeed", 5, grade="e")
baseSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

baseSettings.set("minSpeedToSlice", 5 , grade="e")
baseSettings.set("minSpeedToSlice", 8 , grade="d")
baseSettings.set("minSpeedToSlice", 10 , grade="c") 
baseSettings.set("minSpeedToSlice", 12 , grade="b") 
baseSettings.set("minSpeedToSlice", 12 , grade="a") 

#print(baseSettings.getAll()["minSpeedToSlice"])


baseOutput = base.walkRolledMod(baseSettings.getAll())

baseEnergyCost= -baseOutput.budget.getModEnergy()
baseCreditCost= -baseOutput.budget.getCredits()




print("base costs", baseOutput.budget.getAll())
#print("EF", baseEnergyFactor, "Final credits balance", baseOutput.finalCreditsBalance)
print()
print("budget minus analysis")
#print(base.budget.getAll())
#print("vs x",baseEnergyFactor)
print(baseOutput.budget.getAll())
print()
#budgetcompare=base.budget.compareToBudget(baseOutput.budget, -baseEnergyFactor)
#print(budgetcompare)
#for x in ["amplifier","capacitor","modulator","module","unit","resistor","microprocessor"]:
#    print(x,":",budgetcompare[x])


########################
compareSettings=SimSettings()
compare=modsimulation.ModSimulation()

compareSettings.set("uncoverStatsLimit", 0, grade="e")
compareSettings.set("minInitialSpeed", 5, grade="e")
compareSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

compareSettings.set("minSpeedToSlice", 8 , grade="d")
compareSettings.set("minSpeedToSlice", 10 , grade="c") 
compareSettings.set("minSpeedToSlice", 13 , grade="b") 
compareSettings.set("minSpeedToSlice", 15 , grade="a") 


compareSettings.set("uncoverStatsLimit", 3, grade="e", shape="triangle")
#compareSettings.set("minInitialSpeed", 5, grade="e")
#compareSettings.set("minSpeedToKeep", 10 )

#compareSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])
#compareSettings.set("minSpeedToSlice", 5 , grade="e")
compareSettings.set("minSpeedToSlice", 7 , grade="d", shape="triangle")
compareSettings.set("minSpeedToSlice", 9 , grade="c", shape="triangle")
compareSettings.set("minSpeedToSlice", 12 , grade="b", shape="triangle")



compareOutput=compare.walkRolledMod(compareSettings.getAll())

compareEnergyCost=-compareOutput.budget.getModEnergy()
compareCreditCost=-compareOutput.budget.getCredits()


print("base costs", compareOutput.budget.getAll())


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

#print("base weekly credits",baseOutput.budget.getCredits()*baseEnergyFactor)
#print("compare weekly credits",compareOutput.budget.getCredits()*compareEnergyFactor)

#baseOutput.calcScores(baseEnergyFactor)
#compareOutput.calcScores(compareEnergyFactor)


#baseSpeedValue=Distribution.value(baseOutput.speedDistribution)
#compareSpeedValue=Distribution.value(compareOutput.speedDistribution,energyRatio)

#baseFertilityValue=Distribution.value(baseOutput.speedPerSpeedUpDistribution[4])
#compareFertilityValue=Distribution.value(compareOutput.speedPerSpeedUpDistribution[4],energyRatio)

print("base speed   ",baseOutput.speedValue)
print("compare speed",compareOutput.speedValue)
#print("cmp/base     ",compareOutput.divideValues(compareOutput.speedValue,baseOutput.speedValue))
print()


print("base tilt   ",baseOutput.rltilt)
print("compare tilt", compareOutput.rltilt)
print("base tga    ", baseOutput.targetability)
print("compare tga ", compareOutput.targetability)
print("base speed arrows:", baseOutput.speedArrowProbability*baseEnergyFactor)
print("compare speed arrows:", compareOutput.speedArrowProbability*compareEnergyFactor)



