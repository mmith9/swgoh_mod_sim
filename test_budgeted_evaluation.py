from simSettings import SimSettings
from budgeted_evaluation import *

simSettings=SimSettings()

simSettings.set("uncoverStatsLimit", 2, grade="e")
simSettings.set("minInitialSpeed", 5, grade="e")
simSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

simSettings.set("minSpeedToSlice", 5 , grade="e")
simSettings.set("minSpeedToSlice", 8 , grade="d")
simSettings.set("minSpeedToSlice", 10 , grade="c") 
simSettings.set("minSpeedToSlice", 12 , grade="b") 

simSettings.set("minSpeedToSlice", 17 , grade="a") 
simSettings.set("minSpeedToSlice", 14 , grade="a", speedBumps=3) 
simSettings.set("minSpeedToSlice", 15 , grade="a", speedBumps=4) 

evaluation=BudgetedEvaluation()

score=evaluation.evaluateWithBudget(simSettings.getAll())

print (score)
