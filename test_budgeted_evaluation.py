from simSettings import SimSettings
from budgeted_evaluation import *

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

evaluation=BudgetedEvaluation()

score=evaluation.evaluateWithBudget(simSettings.getAll())




print()
for x in score:
    print(x,":",score[x])

print()
for x in score["budgetBreakdown"]:
    print(x," : ",score["budgetBreakdown"][x])
