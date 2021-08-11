from modsimulation_heat import ModSimulation
from modAnalysis_heat import *

from mod import *
from simSettings import *
from modStore import ModStore
from copy import deepcopy

## simulate weekly budget
class BudgetedEvaluation:
   
    def __init__(self, heat={"mode":"singleSim", "iterateList":False}):
        self.testlevel=0
        self.modSimulation=ModSimulation(heat)
        pass

    def evaluateWithBudget(self, settings):

        #simRoll=ModSimulation()

        initialBudget=Budget()
        initialBudget.calculateWeeklyBudget()
        
        if self.testlevel>10:
            print(initialBudget.getAll())
    
        if settings["general"]["creditsLimit"]=="half":
            initialBudget.set({"credits": initialBudget.getCredits()/2 })
        elif settings["general"]["creditsLimit"] >0:
            initialBudget.set({"credits":settings["general"]["creditsLimit"]})

        if settings["general"]["shipCreditsLimit"]=="half":
            initialBudget.set({"shipCredits": initialBudget.get("shipCredits") /2 })
        elif settings["general"]["shipCreditsLimit"] >0:
            initialBudget.set({"shipCredits":settings["general"]["shipCreditsLimit"]})

        if self.testlevel>10:
            print(initialBudget.getAll())

        initialBudget.convert4BaseSlicingMatsToEnergy()

        if self.testlevel>10:
            print(initialBudget.getAll())

        rolledModAnalysis=self.modSimulation.walkRolledMod(settings)

        wishList=settings["modStore"]["wishList"]

        modStore=ModStore()
        boughtItems=modStore.modShopping(wishList)

        item=boughtItems[0]

        #simBuy=ModSimulation()
        boughtModAnalysis=self.modSimulation.walkBoughtMod(1, item["mod"], settings)
        
        if self.testlevel>20:
            for x in item:
                print(item[x])

        budgetR=rolledModAnalysis.budget
        budgetB=boughtModAnalysis.budget
        
        budgetR.reverseCosts()
        budgetB.reverseCosts()
        budgetBS=deepcopy(budgetB) # mod bought for ship credits has same distribution and costs
        
        budgetB.applyChange({"credits": modStore.getModPrice("credits")})
        budgetBS.applyChange({"shipCredits": modStore.getModPrice("shipCredits")})

        budgetRAllCosts=budgetR.getAll()
        budgetBAllCosts=budgetB.getAll()
        
        if self.testlevel>10:
            print("budget for things")
            print(initialBudget.getAll())

            print("rolled mod cost")
            print(budgetR.getAll())

            print("bought for credits mod cost")
            print(budgetB.getAll())

            print("bought for ship credits mod cost")
            print(budgetBS.getAll())


        ## first spend all ship credits
        wannaBuyShip=initialBudget.get("shipCredits") / budgetBS.get("shipCredits")
        tryToFit=Budget()
        tryToFit.addBudget(budgetBS, wannaBuyShip)
        deficit=initialBudget.canAfford(tryToFit)
        if self.testlevel>10:
            print("ship credits buy deficit", deficit)
        assert(deficit == {}) #should afford all!
        initialBudget.addBudget(budgetBS, - wannaBuyShip)

        finalAnalysis=ModAnalysis()
        finalAnalysis.addAnalysis(boughtModAnalysis, wannaBuyShip)

        if self.testlevel>10:
            print("initial budget after ship credits spent", initialBudget.getEssential())


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

            if False :
                pass

            elif "credits" in deficit:
                if energyFactor > creditsFactor /(2**4):
                    energyFactor/= 2
                    if self.testlevel>10:
                        print("R cut")
                else:
                    creditsFactor/= 2
                    if self.testlevel>10:                        
                        print("B cut")

            elif "modEnergy" in deficit:
                energyFactor/= 2
                if self.testlevel>10:
                    print("R cut")

            elif ("module" in deficit) or ("unit" in deficit) or("resistor" in deficit) or ("microprocessor" in deficit):
                if energyFactor > creditsFactor /2 :
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
                    capacitorAmplifierConverted+= -deficit["amplifier"]/2
                else:
                    initialBudget.energyToMaterial("amplifier", -deficit["amplifier"])
                    capacitorAmplifierConverted+= -deficit["amplifier"]

            elif "capacitor" in deficit:
                if deficit["capacitor"] < -1:
                    initialBudget.energyToMaterial("capacitor", -deficit["capacitor"]/2)
                    capacitorAmplifierConverted+= -deficit["capacitor"]/2
                else:
                    initialBudget.energyToMaterial("capacitor", -deficit["capacitor"])
                    capacitorAmplifierConverted+= -deficit["capacitor"]

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
                
                    ## recalculate what you can buy for credits due to energy expenses
                    tmpMaxRoll=initialBudget.getModEnergy() / budgetR.getModEnergy() 
                    tmpMaxBuy=(initialBudget.getCredits() - budgetR.getCredits()*tmpMaxRoll) / budgetB.getCredits()

                    creditsFactor= tmpMaxBuy / wannaBuy

                    if creditsFactor < 0:   ## floating point errors cause negative value from above calculations
                        creditsFactor= 0

                    if self.testlevel>10:
                        print(tmpMaxRoll)
                        print(tmpMaxBuy)
                        print(wannaBuy)
                        print(creditsFactor)

                    assert(creditsFactor>=0)
                
                if self.testlevel>10:
                    print(budgetR.getEssential())
                    print(budgetB.getEssential())
           
            if self.testlevel>10:
                print("capacitor or amplifier bought", capacitorAmplifierConverted)
            if self.testlevel>20:
                input("Press Enter to continue...")
            
            maxTries-= 1
            #endTries=maxTries

            if initialBudget.getModEnergy() < 1 :
                maxTries= -1
            if energyFactor< 1/(2**30) and creditsFactor< 1/(2**30):
                maxTries= -1
        
        if self.testlevel>9:
            print("FINAL")
            print("Roll", wannaRoll*Rbought)
            print("Buy", wannaBuy*Bbought, "plus ship", wannaBuyShip)

        #print(endTries)
        finalAnalysis.addAnalysis(rolledModAnalysis, wannaRoll*Rbought )
        finalAnalysis.addAnalysis(boughtModAnalysis, wannaBuy*Bbought )
        finalAnalysis.calcScores()
        finalScore=finalAnalysis.getScores()      

        budgetBreakdown={}
        budgetBreakdown["budgetRemaining"]=initialBudget.getAll()
        budgetBreakdown["budgetRoll"]=budgetRAllCosts
        budgetBreakdown["budgetBuy"]=budgetBAllCosts
        budgetBreakdown["BudgetRollBought"]=wannaRoll*Rbought
        budgetBreakdown["BudgetBuyBought"]=wannaBuy*Bbought
        budgetBreakdown["Rbought"]=Rbought
        budgetBreakdown["Bbought"]=Bbought
        budgetBreakdown["BSbought"]=wannaBuyShip
        budgetBreakdown["capAmpBought"]=capacitorAmplifierConverted

        finalScore["budgetBreakdown"]=budgetBreakdown
        
        return finalScore






