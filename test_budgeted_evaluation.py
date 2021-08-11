from simSettings import SimSettings
import budgeted_evaluation
import budgeted_evaluation_heat
import processJobs_heat
import json
import time

simSettings=SimSettings()

simSettings.set("minSpeedToSlice", 100, grade="any", shape="any", speedBumps="any")
simSettings.set("minSpeedToSlice", 18 , grade=["6e","6d","6c","6b"], speedBumps=4) 
simSettings.set("minSpeedToSlice", 15 , grade=["6e","6d","6c","6b"], speedBumps=3) 

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

simSettings.set("minSpeedToSlice", 100 , grade="any", speedBumps=5) 
simSettings.set("minSpeedToSlice", 100 , grade="a", speedBumps=1) 
simSettings.set("minSpeedToSlice", 100 , grade="b", speedBumps=1) 
simSettings.set("minSpeedToSlice", 100 , grade="c", speedBumps=1) 
simSettings.set("minSpeedToSlice", 100 , grade="d", speedBumps=1) 

simSettings.set("minSpeedToSlice", 100 , grade="a", speedBumps=2) 

simSettings.set("minSpeedToSlice", 100 , grade="e", speedBumps=2) 
simSettings.set("minSpeedToSlice", 100 , grade="e", speedBumps=3) 
simSettings.set("minSpeedToSlice", 100 , grade="e", speedBumps=4) 


simSettings.set("minSpeedToSlice", 100 , grade="d", speedBumps=3) 
simSettings.set("minSpeedToSlice", 100 , grade="d", speedBumps=4) 

simSettings.set("minSpeedToSlice", 100 , grade="c", speedBumps=4) 

simSettings.general["creditsLimit"] = 11000000
simSettings.general["shipCreditsLimit"] = 2500000


iterateList=[
    {"target":"uncoverStatsLimit", "range":[0] , "shape":"any", "grade":"e", "speedBumps":0},  
    {"target":"minInitialSpeed", "range":[5] , "shape":"any", "grade":"e", "speedBumps":0},  # 5 is always the best
    
    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"d", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[8,9,10] , "shape":"any", "grade":"d", "speedBumps":2},

    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"c", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[8,9,10], "shape":"any", "grade":"c", "speedBumps":2},
    {"target":"minSpeedToSlice", "range":[10,11,12,13,14,15] , "shape":"any", "grade":"c", "speedBumps":3},
       
    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"b", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[9,10,11], "shape":"any", "grade":"b", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[10,11,12,13,14,15], "shape":"any", "grade":"b", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[13,14,15,16,17,18] , "shape":"any", "grade":"b", "speedBumps":4}, #never shows 18

    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"a", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[10,11,12] , "shape":"any", "grade":"a", "speedBumps":2},  # no use, always pops 12 in top 100 scores
    {"target":"minSpeedToSlice", "range":[12,13,14,15], "shape":"any", "grade":"a", "speedBumps":3},
    {"target":"minSpeedToSlice", "range":[13,14,15,16,17,18] , "shape":"any", "grade":"a", "speedBumps":4},   #never shows 18

    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6e", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6d", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6c", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6b", "speedBumps":2}, 

    {"target":"minSpeedToSlice", "range":[14,15,16] , "shape":"any", "grade":"6e", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[14,15,16] , "shape":"any", "grade":"6d", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[14,15,16] , "shape":"any", "grade":"6c", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[15,16,17,18] , "shape":"any", "grade":"6b", "speedBumps":3}, 

    {"target":"minSpeedToSlice", "range":[13,15,16,17,18,19] , "shape":"any", "grade":"6e", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[13,15,16,17,18,19] , "shape":"any", "grade":"6d", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[13,15,16,17,18,19] , "shape":"any", "grade":"6c", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[13,15,16,17,18,19] , "shape":"any", "grade":"6b", "speedBumps":4}, 
]



def printDictsDifferences(dict1:dict, dict2:dict, depthString=""):
    for key in dict1:
        if key in dict2.keys():
            if type(dict1[key]) is dict:
                printDictsDifferences(dict1[key], dict2[key], depthString+str(key)+"/")
            elif type(dict1[key]) in [int, float] :
                if type(dict2[key]) in [int, float]:
                    
                    diff=dict1[key]-dict2[key]
                    if True: #abs(diff) >0.000001:
                        print(depthString+str(key), dict1[key]-dict2[key], end="|")
            else:
                print(depthString,type(dict1), end="|")

settings=json.loads(json.dumps(simSettings.getAll()))


evaluation=budgeted_evaluation.BudgetedEvaluation()

score=evaluation.evaluateWithBudget(settings)
print()
print("HEAT OFF")
print()
for x in score:
    print(x,":",score[x])

print()
for x in score ["budgetBreakdown"]:
    print(x," : ",score["budgetBreakdown"][x])

print()
print("HEAT ON")
print()
evaluation=budgeted_evaluation_heat.BudgetedEvaluation(heat={"mode":"multiSim", "iterateList":iterateList})

score_heat=evaluation.evaluateWithBudget(settings)



print()
for x in score_heat:
    print(x,":",score[x])

print()
for x in score_heat ["budgetBreakdown"]:
    print(x," : ",score["budgetBreakdown"][x])

print("DIFFERENCES")
printDictsDifferences(score, score_heat)
print()


proc=processJobs_heat.JobsProcessing()
tmpList=[{"job":"test", "scores": score_heat, "settings": settings }]
proc.displayResultsRelevantSettings(tmpList,1)

benchmark=budgeted_evaluation_heat.BudgetedEvaluation(heat={"mode":"multiSim", "iterateList":iterateList})

start_time = time.time()
results=[]

benchmark=budgeted_evaluation_heat.BudgetedEvaluation(heat={"mode":"multiSim", "iterateList":iterateList})            
for repeats in range(0,100):
    
    result=benchmark.evaluateWithBudget(settings)
    results.append((benchmark, result))

timeDiff=time.time() - start_time

print(timeDiff, "seconds")

print(100/timeDiff, "sims per secon")

