from modsimulation import ModSimulation
from modAnalysis import *

from mod import *
from simSettings import *
from modStore import ModStore


## simulate weekly budget
class BudgetedEvaluation:
   
    def __init__(self):
        self.testlevel=0
        pass

    def evaluateWithBudget(self, settings):

        simRoll=ModSimulation()

        initialBudget=Budget()
        initialBudget.calculateWeeklyBudget()
    
        if settings["general"]["creditsLimit"]=="half":
            initialBudget.set({"credits": initialBudget.getCredits()/2 })
        elif settings["general"]["creditsLimit"]>0:
            initialBudget.set({"credits":settings["general"]["creditsLimit"]})

        if self.testlevel>10:
            print(initialBudget.getAll())

        initialBudget.convert4BaseSlicingMatsToEnergy()

        if self.testlevel>10:
            print(initialBudget.getAll())

        rolledModAnalysis=simRoll.walkRolledMod(settings)
        

        wishList=settings["modStore"]["wishList"]

        modStore=ModStore()
        boughtItems=modStore.modShopping(wishList)

        item=boughtItems[0]

        simBuy=ModSimulation()
        boughtModAnalysis=simBuy.walkBoughtMod(1, item["mod"], settings)
        boughtModAnalysis.budget.applyChange({"credits": -item["creditCost"]})

        budgetR=rolledModAnalysis.budget
        budgetB=boughtModAnalysis.budget

        budgetR.reverseCosts()
        budgetB.reverseCosts()

        budgetRAllCosts=budgetR.getAll()
        budgetBAllCosts=budgetB.getAll()
        
        if self.testlevel>10:
            print("budget for things")
            print(initialBudget.getAll())

            print("rolled mod cost")
            print(budgetR.getAll())

            print("bought mod cost")
            print(budgetB.getAll())

        Rbought=0
        Bbought=0
        energyFactor=1
        creditsFactor=1
        maxTries=500
        capacitorAmplifierConverted=0

        wannaRoll=initialBudget.getModEnergy() / budgetR.getModEnergy() 
        wannaBuy=(initialBudget.getCredits() - budgetR.getCredits()*wannaRoll) / budgetB.getCredits()

        while maxTries>0:
            if self.testlevel>10:
                print("tries left :",maxTries)

            tryToFit=Budget()
            tryToFit.addBudget(budgetR, energyFactor * wannaRoll)
            tryToFit.addBudget(budgetB, creditsFactor * wannaBuy)
            deficit=initialBudget.canAfford(tryToFit)

            if self.testlevel>10:
                print("Budget to buy")
                print(initialBudget.getEssential())
                print("trying to buy")
                print(tryToFit.getEssential())
                print("deficit")
                print(deficit)
                print("roll",wannaRoll, " buy", wannaBuy)
                print("Rfactor", energyFactor, "R bought", Rbought)
                print("Bfactor", creditsFactor, "B bought", Bbought)

            if "modEnergy" in deficit:
                energyFactor/= 2
                if self.testlevel>10:
                    print("R cut")


            elif "credits" in deficit:
                creditsFactor/= 2
                if self.testlevel>10:
                    print("B cut")

            elif "modEnergy" in deficit:
                energyFactor/= 2
                if self.testlevel>10:
                    print("R cut")

            elif ("module" in deficit) or ("unit" in deficit) or("resistor" in deficit) or ("microprocessor" in deficit):
                if energyFactor > creditsFactor :
                    energyFactor/= 2
                    if self.testlevel>10:
                        print("R cut")
                else:
                    creditsFactor/= 2
                    if self.testlevel>10:                        
                        print("B cut")

            elif "amplifier" in deficit:
                if deficit["amplifier"] < -1:
                    initialBudget.energyToMaterial("amplifier", -deficit["amplifier"]/2)
                    capacitorAmplifierConverted+=-deficit["amplifier"]/2
                else:
                    initialBudget.energyToMaterial("amplifier", -deficit["amplifier"])
                    capacitorAmplifierConverted+=-deficit["amplifier"]
            elif "capacitor" in deficit:
                if deficit["capacitor"] < -1:
                    initialBudget.energyToMaterial("capacitor", -deficit["capacitor"]/2)
                    capacitorAmplifierConverted+=-deficit["capacitor"]/2
                else:
                    initialBudget.energyToMaterial("capacitor", -deficit["capacitor"])
                    capacitorAmplifierConverted+=-deficit["capacitor"]

            else:

                if initialBudget.getCredits() < budgetR.getCredits()*energyFactor*wannaRoll + budgetB.getCredits()*creditsFactor*wannaBuy :
                    creditsFactor/= 2
                    if self.testlevel>10:
                        print("B overspending cut")

                else:
                    #assert(deficit=={} )
                    initialBudget.addBudget(budgetR, - energyFactor * wannaRoll)
                    Rbought+= energyFactor
                    initialBudget.addBudget(budgetB, - creditsFactor * wannaBuy)
                    Bbought+= creditsFactor
                    if self.testlevel>10:
                        print("Bought",energyFactor, creditsFactor)

                    if Rbought==1 :
                        energyFactor=0
                    if Bbought==1 :
                        creditsFactor=0
                
                #print(budgetR.getEssential())
                #print(budgetB.getEssential())
                
            
            if self.testlevel>10:
                print("capacitor or amplifier bought", capacitorAmplifierConverted)
                #input("Press Enter to continue...")
            maxTries-= 1

            if initialBudget.getModEnergy() < 1 :
                maxTries= -1
            if energyFactor< 1/(2**30) and creditsFactor< 1/(2**30):
                maxTries= -1
        
        if self.testlevel>10:
            print("FINAL")
            print("Roll", wannaRoll*Rbought)
            print("Buy", wannaBuy*Bbought)

        finalAnalysis=ModAnalysis()
        finalAnalysis.addAnalysis(simRoll.analysis, wannaRoll*Rbought )
        finalAnalysis.addAnalysis(simBuy.analysis, wannaBuy*Bbought )
        finalAnalysis.calcScores()
        finalScore=finalAnalysis.getScores()      

        finalScore["budgetRoll"]=budgetRAllCosts
        finalScore["budgetBuy"]=budgetBAllCosts
        finalScore["budgetremaining"]=initialBudget.getAll()
        finalScore["capacitorAmplifierConverted"]=capacitorAmplifierConverted
        
        return finalScore






