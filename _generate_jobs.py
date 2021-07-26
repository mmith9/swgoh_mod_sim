from simSettings import *

test=SimSettings()

test.set("uncoverStatsLimit", 2, grade="e")
test.set("minInitialSpeed", 5, grade="e")
test.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

test.set("minSpeedToSlice", 5 , grade="e")
test.set("minSpeedToSlice", 8 , grade="d")
test.set("minSpeedToSlice", 12 , grade="c")
test.set("minSpeedToSlice", 14 , grade="b")
test.set("minSpeedToSlice", 17 , grade="a") 


iterateList=[

#    {"target":"minSpeedToSlice", "range":[6,7,8,9,10] , "shape":"any", "grade":"d", "speedBumps":2},

    {"target":"minSpeedToSlice", "range":[8,9,10] , "shape":"any", "grade":"c", "speedBumps":2},
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"c", "speedBumps":3},
       
    {"target":"minSpeedToSlice", "range":[9,10,11] , "shape":"any", "grade":"b", "speedBumps":2},
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"b", "speedBumps":3},
    {"target":"minSpeedToSlice", "range":[13,14,15,16,17] , "shape":"any", "grade":"b", "speedBumps":4},

    {"target":"minSpeedToSlice", "range":[12,13,14,15,16] , "shape":"any", "grade":"a", "speedBumps":3},
    {"target":"minSpeedToSlice", "range":[14,15,16,17] , "shape":"any", "grade":"a", "speedBumps":4}

]

output=test.iterate(iterateList, outputPrefix="ITER01x", fileCut=1000)

print(output)
