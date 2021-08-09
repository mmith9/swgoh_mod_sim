from simSettings import SimSettings
import budgeted_evaluation
import budgeted_evaluation_heat

simSettings=SimSettings()

simSettings.set("uncoverStatsLimit", 3, grade="e")
simSettings.set("minInitialSpeed", 5, grade="e")
simSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

simSettings.set("minSpeedToSlice", 5 , grade="e")
simSettings.set("minSpeedToSlice", 9 , grade="d")

simSettings.set("minSpeedToSlice", 10 , grade="c") 
simSettings.set("minSpeedToSlice", 13 , grade="c", speedBumps=3) 

simSettings.set("minSpeedToSlice", 10 , grade="b") 
simSettings.set("minSpeedToSlice", 13 , grade="b", speedBumps=3) 
simSettings.set("minSpeedToSlice", 14 , grade="b", speedBumps=4) 


simSettings.set("minSpeedToSlice", 17 , grade="a") 
simSettings.set("minSpeedToSlice", 14 , grade="a", speedBumps=3) 
simSettings.set("minSpeedToSlice", 17 , grade="a", speedBumps=4) 

simSettings.general["creditsLimit"] = 11000000
simSettings.general["shipCreditsLimit"] = 2500000

def printDictsDifferences(dict1:dict, dict2:dict, depthString=""):
    for key in dict1:
        if type(dict1[key]) is dict:
            printDictsDifferences(dict1[key], dict2[key], depthString+str(key)+"/")
        elif type(dict1[key]) in [int, float] :
            diff=dict1[key]-dict2[key]
            if abs(diff) >0.000001:
                print(depthString+str(key), dict1[key]-dict2[key], end="|")
        else:
            print(depthString,type(dict1), end="|")


evaluation=budgeted_evaluation.BudgetedEvaluation()

score=evaluation.evaluateWithBudget(simSettings.getAll())

print()
for x in score:
    print(x,":",score[x])

print()
for x in score ["budgetBreakdown"]:
    print(x," : ",score["budgetBreakdown"][x])


evaluation=budgeted_evaluation_heat.BudgetedEvaluation()

score_heat=evaluation.evaluateWithBudget(simSettings.getAll())

print()
for x in score_heat:
    print(x,":",score[x])

print()
for x in score_heat ["budgetBreakdown"]:
    print(x," : ",score["budgetBreakdown"][x])

printDictsDifferences(score, score_heat)
print()




        
